__author__ = 'quybvs'

from ebooklib import epub
from model.book import Book
from datetime import datetime
from PIL import Image
import requests

import cStringIO

from config.logging_cfg import *
from config.system_cfg import VNTQ_COPYRIGHT_STRING


class Burner:
    book = None

    def __init__(self, book=None):
        if book:
            self.book = book

    def burning(self):
        epub_book = epub.EpubBook()
        if self.book and isinstance(self.book, Book):
            epub_book.set_title(self.book.title + " " + VNTQ_COPYRIGHT_STRING)
            epub_book.set_language('vn')
            epub_book.add_author(self.book.author)
            epub_book.set_identifier(self.book.title + self.book.author)

            # get cover image file
            if self.book.thumb:
                try:
                    rs = requests.get(self.book.thumb)
                    image_obj = Image.open(cStringIO.StringIO(rs.content))
                    epub_book.set_cover('cover.' + image_obj.format, rs.content)
                except requests.exceptions.ConnectionError:
                    log.error("Can't download cover image from %s", self.book.thumb)

            chapter_order = 1
            epub_book.add_item(epub.EpubNcx())
            epub_book.add_item(epub.EpubNav())
            epub_book.spine.append('nav')

            for chapter in self.book.chapters:
                epub_chapter = epub.EpubHtml(uid='chap_' + str(chapter_order), title=chapter.title,
                                             file_name='chap_' + str(chapter_order) + '.xhtml',
                                             content=chapter.content, lang='vn')
                epub_book.add_item(epub_chapter)
                epub_book.toc.append(
                    epub.Link('chap_' + str(chapter_order) + '.xhtml', chapter.title, 'chap_' + str(chapter_order)))
                epub_book.spine.append(epub_chapter)
                chapter_order += 1

            # define CSS style
            style = 'BODY {color: white;}'
            nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

            # add CSS file
            epub_book.add_item(nav_css)

            epub.write_epub(
                '[' + datetime.strftime(datetime.now(), '%Y_%m_%d_%H_%M_%S') + ']' + self.book.title + '.epub',
                epub_book,
                {})
            return True
        else:
            return False
