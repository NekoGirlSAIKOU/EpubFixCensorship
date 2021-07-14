from typing import List, Optional

from autoreplace import AutoReplace

from ebooklib import epub
from lxml import etree


class Chapter:
    def __init__(self, title: str, content: etree._Element, censored_elements: List[etree._Element] = ...):
        self.title = title
        self.content = content
        if self.title is ... or self.title is None or self.title == "":
            try:
                self.title = self.content.xpath('/html/head/title//text()')[0]
            except IndexError:
                pass

        self.censored_elements: List[etree._Element] = [] if censored_elements is ... else censored_elements


class EpubCensorshipFixer:
    def __init__(self, book: epub.EpubBook, replacer: AutoReplace,
                 element_tags: List[str] = ...,
                 element_strings: List[str] = ...,
                 check_element_by_rules=False):
        self.book = book
        self.chapters: List[Optional[Chapter]] = []
        self.censored_element: List[etree._Element] = []
        self.censored_element_chapter_title: List[str] = []
        self.censored_element_chapter: List[Chapter] = []
        self.replacer = replacer

        self.element_tags = ['p'] if element_tags is ... else element_tags
        self.element_strings = ['*'] if element_strings is ... else element_strings
        self.check_element_by_rules = check_element_by_rules

        # Load items
        for item in self.book.spine:
            if isinstance(item,tuple):
                item = self.book.get_item_with_id(item[0])

            if isinstance(item, epub.EpubHtml):
                self.chapters.append(Chapter(title=item.title, content=etree.HTML(item.content)))
                self.chapters[-1].censored_elements = self.filter_content(self.chapters[-1].content)
                self.censored_element.extend(self.chapters[-1].censored_elements)
                self.censored_element_chapter_title.extend(
                    [self.chapters[-1].title] * len(self.chapters[-1].censored_elements))
                self.censored_element_chapter.extend(
                    [self.chapters[-1]] * len(self.chapters[-1].censored_elements)
                )
            else:
                self.chapters.append(None)

    @property
    def chapters_all(self):
        return list(i for i in self.chapters if i is not None)

    @property
    def chapters_censored(self):
        return list(i for i in self.chapters if i is not None and len(i.censored_elements) > 0)

    def filter_content(self, content: etree._Element):
        elements: List[etree._Element] = content.cssselect(','.join(self.element_tags))
        r: List[etree._Element] = []
        for element in elements:
            if element.text is None:
                continue
            if element.get('censored_text') is not None:
                r.append(element)
                continue

            will_append = False
            for char in self.element_strings:
                if char in element.get('censored_text', element.text):
                    will_append = True
                    continue
            if will_append:
                r.append(element)
                del will_append
                continue

            del will_append

            if self.check_element_by_rules:
                replaced_texts = self.replacer.replace_text(element.text)
                if len(replaced_texts) > 1:
                    r.append(element)
                    continue
        return r

    def regenerate_epub_item(self):
        for i in range(len(self.chapters)):
            chapter = self.chapters[i]
            item = self.book.spine[i]
            if chapter is None:
                pass
            else:
                if isinstance(item,tuple):
                    item = self.book.get_item_with_id(item[0])
                assert isinstance(item, epub.EpubHtml)
                item.content = etree.tounicode(chapter.content)
                item.title = chapter.title
