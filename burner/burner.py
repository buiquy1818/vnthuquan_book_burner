__author__ = 'quybvs'

from ebooklib import epub
from model.book import Book
from datetime import datetime
from PIL import Image
import requests

import cStringIO

from config.logging_cfg import *
from config.system_cfg import VNTQ_COPYRIGHT_STRING, UPPER_CHAR_URL, UPPER_CHAR_PATH


class Burner:
    book = None

    def __init__(self, book=None):
        if book:
            self.book = book

    def burning(self):
        epub_book = epub.EpubBook()
        if self.book and isinstance(self.book, Book):
            epub_book.set_title(self.book.title + " (" + VNTQ_COPYRIGHT_STRING + ") ")
            epub_book.set_language('vn')
            epub_book.add_author(self.book.author)
            epub_book.set_identifier(self.book.title + self.book.author)

            # get cover image file
            if self.book.thumb:
                try:
                    rs = requests.get(self.book.thumb, stream=True)
                    image_obj = Image.open(cStringIO.StringIO(rs.content))
                    epub_book.set_cover('cover.' + image_obj.format, rs.content)
                    log.info("Book cover is created")
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

                # add upper character
                upper_character_list = []
                if chapter.upper_character:
                    if chapter.upper_character not in upper_character_list:
                        upper_character_list.append(chapter.upper_character)
                        try:
                            rs = requests.get(UPPER_CHAR_URL + chapter.upper_character, stream=True)

                            upper_char_img = epub.EpubItem(uid=chapter.upper_character,
                                                           file_name=UPPER_CHAR_PATH + chapter.upper_character,
                                                           content=rs.content)
                            # add upper character to book
                            epub_book.add_item(upper_char_img)
                            log.info("Add upper character img: " + chapter.upper_character)
                        except requests.exceptions.ConnectionError:
                            log.error("Can't download upper char image from %s", chapter.upper_character)

            # define CSS style
            style = 'BODY {color: white;}'
            nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
            epub_book.add_item(nav_css)

            epub.write_epub(
                '[' + datetime.strftime(datetime.now(), '%Y_%m_%d_%H_%M_%S') + ']' + self.book.title + '.epub',
                epub_book,
                {})
            return True
        else:
            return False
