# -*- coding: utf-8 -*-
__author__ = 'quybvs'

from bs4 import BeautifulSoup
import requests
import re
import time

import sys

reload(sys)
sys.setdefaultencoding('utf8')

from config.logging_cfg import *
from config import system_cfg
from model.book import Book
from model.chapter import Chapter
from library import html_tool


class Crawler:
    book = None
    status = None

    def __init__(self, root_url):
        self.root_url = root_url
        self.book = Book()
        self.status = False

    def set_root_url(self, url):
        self.root_url = url

    def crawling(self):
        self.book = Book()  # Reinitialize Book object for retry
        log.info("Crawling function is call")
        if self.root_url:
            thumb, title, author, chapter_params = self.get_general_info()

            if Book.general_validate(title, author, chapter_params):
                self.book.set_thumb(thumb)
                self.book.set_title(title)
                self.book.set_author(author)
                for chapter_param in chapter_params:
                    chapter = self.get_chapter(chapter_param)
                    if not Book.chapter_validate(chapter):
                        log.error("Chapter: %s is fail crawled", chapter)
                        return False
                    self.book.add_chapter(chapter)

                self.status = True
                return True
            else:
                log.error("No validate general info")
                return False
        else:
            log.error("not define root url")
            return False

    def get_general_info(self):
        log.info("get_general_info function is call")
        book_thumb = None
        book_title = None
        book_author = None
        chapter_params = []

        # site_rs = requests.get(self.root_url, verify=False)
        site_rs = self.try_request(self.root_url)

        soup = BeautifulSoup(site_rs.content, 'html.parser')

        for acronym in soup.find_all('acronym'):
            chapter_link = acronym.li.get('onclick')

            if chapter_link:
                chapter_re = re.search('noidung1\(\'((\w|\W)*)\'\)', chapter_link)
                chapter_param = chapter_re.group(1)
                chapter_params.append(chapter_param)

        if chapter_params:
            first_chapter = self.get_chapter(chapter_params[0])
            if first_chapter.book_thumb:
                book_thumb = first_chapter.book_thumb
            if first_chapter.book_title:
                book_title = first_chapter.book_title
            if first_chapter.book_author:
                book_author = first_chapter.book_author

        return book_thumb, book_title, book_author, chapter_params

    def get_chapter(self, chapter_param):
        log.info("get_chapter function is call")
        log.info(chapter_param)

        book_title = None
        book_thumb = None
        book_author = None
        chapter_title = None
        chapter_content = None

        url = system_cfg.CHAPTER_URL
        chapter_param = html_tool.decode_param_to_dict(chapter_param)
        site_rs = self.try_request(url, 'POST', data=chapter_param)

        content_list = site_rs.content.split('--!!tach_noi_dung!!--', 3)
        if len(content_list) >= 3:

            #####################
            # get book_thumb from css
            #####################
            css_soup = BeautifulSoup(content_list[0], 'html.parser')
            style_tag = css_soup.find('style')
            if style_tag:
                thumb_re = re.search('background:url\((http://(\w|\W)*)\)', style_tag.string)
                if thumb_re:
                    book_thumb = thumb_re.group(1)

            #####################
            # get book title
            # get book author
            # get chapter title
            #####################
            desc_soup = BeautifulSoup(content_list[1], 'html.parser')
            tieude0anh_tag = desc_soup.find('div', class_='tieude0anh')

            if tieude0anh_tag:
                book_title_tag = desc_soup.find('span', class_='chuto40')
                if book_title_tag:
                    book_title = book_title_tag.string.strip()
                tac_gia_tag = desc_soup.find('span', class_='tacgiaphai')
                if tac_gia_tag:
                    book_author = tac_gia_tag.string.strip()

                chutieude_tags = desc_soup.find_all('span', class_='chutieude')
                chutieude_list = []
                for chutieude_tag in chutieude_tags:
                    if chutieude_tag.text and chutieude_tag.text.strip():
                        chutieude_list.append(chutieude_tag.text.strip())
                if len(chutieude_list) == 2:
                    chapter_title = chutieude_list[0] + ": " + chutieude_list[1]
                elif len(chutieude_list) == 1:
                    chapter_title = chutieude_list[0]

            else:
                book_title_tag = desc_soup.find('span', class_='chuto40')
                if book_title_tag:
                    book_title = book_title_tag.string.strip()

                chutieude_tags = desc_soup.find_all('span', class_='chutieude')
                chutieude_list = []
                for chutieude_tag in chutieude_tags:
                    if chutieude_tag.string and chutieude_tag.string.strip():
                        chutieude_list.append(chutieude_tag.string.strip())
                if len(chutieude_list) == 2:
                    book_author = chutieude_list[0]
                    chapter_title = chutieude_list[1]
                elif len(chutieude_list) == 1:
                    chapter_title = chutieude_list[0]

            #####################
            # get chapter content( add chapter title to chapter content)
            #####################

            chapter_content = content_list[2]

            first_character_re = re.search(
                '<div id="chuhoain"(\w|\W)*cotich_(\w)(\w|\W)*?<br(\w|\W)*?>((\w|\W)*)', chapter_content)
            if first_character_re:
                chapter_content = first_character_re.group(2) + first_character_re.group(5)

            # Add chapter title to chapter_content
            if chapter_title and chapter_content:
                chapter_content = '<div><h2 align=\'center\'>' + chapter_title + '</h2></div>' + chapter_content

        chapter = Chapter(title=chapter_title, content=chapter_content)
        if book_title:
            chapter.set_book_title(book_title)
        if book_author:
            chapter.set_book_author(book_author)
        if book_thumb:
            chapter.set_book_thumb(book_thumb)
        log.info("Crawler chapter: %s", chapter_title)

        return chapter

    def try_request(self, url, post_type='GET', try_time=0, params=None, data=None):
        try:

            if post_type == 'GET':
                headers = {'User-Agent': system_cfg.USER_AGENT}
                site_rs = requests.get(url=url, params=params, data=data, headers=headers, verify=False)
            else:

                headers = {'User-Agent': system_cfg.USER_AGENT}
                session = requests.Session()
                session.get(url, headers=headers)
                cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(session.cookies))

                site_rs = requests.post(url=url, params=params, data=data, headers=headers, cookies=cookies,
                                        verify=False)

            if not site_rs:
                raise requests.exceptions.ConnectionError

            return site_rs
        except requests.exceptions.ConnectionError:
            try_time += 1
            if try_time >= system_cfg.MAX_RETRY_TIME:
                return None
            else:
                time.sleep(system_cfg.WAITING_TIME)
                log.warn("Retry url %s %r time" % (url, try_time))
                return self.try_request(url, post_type, try_time, params, data)
