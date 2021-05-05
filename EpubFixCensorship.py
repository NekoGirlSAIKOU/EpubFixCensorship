#!/usr/bin/env python3
import sys
from typing import List
from ebooklib import epub
from lxml import etree
from version import VERSION,VERSION_NAME
from config import init_config
from autoreplace import AutoReplace


def set_book_version_metadata(book:epub.EpubBook):
    book.set_unique_metadata('OPF', 'EpubFixCensorship version','',others={'name': 'EpubFixCensorship version', 'content': VERSION_NAME})

def filter_element(config:dict, replacer:AutoReplace,elements: List[etree._Element]) -> List[etree._Element]:
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
    print("Unavilable for now.")
    return 0


if __name__ == '__main__':
    sys.exit(main())