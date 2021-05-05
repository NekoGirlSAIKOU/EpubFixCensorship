#!/usr/bin/env python3
from ebooklib import epub
from version import VERSION,VERSION_NAME

def set_book_version_metadata(book:epub.EpubBook):
    book.set_unique_metadata('OPF', 'EpubFixCensorship version','',others={'name': 'EpubFixCensorship version', 'content': VERSION_NAME})

