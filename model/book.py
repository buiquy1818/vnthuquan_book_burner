__author__ = 'quybvs'

from model.chapter import Chapter


class Book:
    thumb = None
    title = None
    url = None
    author = None
    chapters = []  # Array of chapter

    def __init__(self, url=None, thumb=None, author=None):
        if url:
            self.url = url
        if thumb:
            self.thumb = thumb
        if author:
            self.author = author

    def set_thumb(self, thumb):
        self.thumb = thumb

    def set_title(self, title):
        self.title = title

    def set_url(self, url):
        self.url = url

    def set_author(self, author):
        self.author = author

    def add_chapter(self, chapter):
        self.chapters.append(chapter)

    @staticmethod
    def general_validate(title, author, chapter_params):
        if title and author and isinstance(chapter_params, list):
            return True
        else:
            return False

    @staticmethod
    def chapter_validate(chapter):
        if isinstance(chapter, Chapter) and chapter.title and chapter.content:
            return True
        else:
            return False
