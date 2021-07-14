#!/usr/bin/env python3
import json
import sys
from typing import List
from ebooklib import epub, ITEM_DOCUMENT
from lxml import etree

from EpubCensorshipFixer import EpubCensorshipFixer
from version import VERSION, VERSION_NAME
from config import init_config, PROGRAM_PATH
from autoreplace import AutoReplace
import argparse


def set_book_version_metadata(book: epub.EpubBook):
    book.set_unique_metadata('OPF', 'EpubFixCensorship version', '',
                             others={'name': 'EpubFixCensorship version', 'content': VERSION_NAME})


def filter_element(config: dict, replacer: AutoReplace, elements: List[etree._Element]) -> List[etree._Element]:
    r: List[etree._Element] = []
    for element in elements:
        if element.text is None:
            continue

        if element.get('censored_text') is not None:
            r.append(element)
            continue

        for char in config['element_strings']:
            if char in element.get('censored_text', element.text):
                r.append(element)
                continue

        if config['check_element_by_rules']:
            replaced_texts = replacer.replace_text(element.text)
            if len(replaced_texts) > 1:
                r.append(element)
                continue

    return r


def main():
    parser = argparse.ArgumentParser(prog='EpubFixCensorship')
    parser.add_argument('book', help="The epub file which should be fixed.")
    parser.add_argument('-r', '--rule', action="store_true", help="Use rules to fix.", dest="use_rule")
    parser.add_argument('-t', '--tags', help="Element tags")
    parser.add_argument('-s', '--texts', help="Element texts")
    parser.add_argument('--check-rule', action='store_true', help="Check element by rules", dest='check_rule')
    parser.add_argument('--no-check-rule', action='store_true', help="Don't check element by rules",
                        dest='no_check_rule')
    parser.add_argument('-o', '--output', help="Save epub to this path. Default is to override input epub.")

    args = parser.parse_args(sys.argv[1:])

    # Deal with config
    with open(f'{PROGRAM_PATH}/config.json', encoding='utf8') as f:
        config = json.load(f)
    init_config(config)
    if args.tags is not None:
        config['element_tags'] = args.tags.split(' ')
    if args.texts is not None:
        config['element_strings'] = args.text.split(' ')
    if args.check_rule:
        config['check_element_by_rules'] = True
    elif args.no_check_rule:
        config['check_element_by_rules'] = False
    if args.use_rule:
        pass
    else:
        config['check_element_by_rules'] = False

    # Init replacer
    if args.use_rule:
        with open(f'{PROGRAM_PATH}/rules.json', encoding='utf8') as f:
            rules = json.load(f)
    else:
        rules = []
    with open(f'{PROGRAM_PATH}/replace_history.json', encoding='utf8') as f:
        history = json.load(f)
    replacer = AutoReplace(rules=rules, replace_histories=history)

    # Load book
    book = epub.read_epub(args.book)
    set_book_version_metadata(book)
    print("Load fixer")
    fixer = EpubCensorshipFixer(book,replacer,
                                element_tags=config['element_tags'],
                                element_strings=config['element_strings'],
                                check_element_by_rules=config['check_element_by_rules'])

    print("Process chapter")
    for element in fixer.censored_element:
        origin_text = element.get("censored_text",element.text)
        print(f"Fix {origin_text}")
        try:
            r = replacer.replace_text(origin_text)[1]
        except IndexError:
            print("Found a text that cant be fixed:")
            print(origin_text)
        else:
            print(f"Apply rule: {r[0]}")
            if element.get('censored_text', None) is None:
                element.set('censored_text', origin_text)
            element.text = r[1]
            print(f"Fix to {r[1]}")

    print("Regenerate chapter item")
    fixer.regenerate_epub_item()

    print("Save epub")
    if args.output is None:
        epub.write_epub(name=args.book, book=book)
    else:
        epub.write_epub(name=args.output, book=book)

    return 0


if __name__ == '__main__':
    sys.exit(main())
