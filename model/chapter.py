__author__ = 'quybvs'


class Chapter:
    book_title = None
    book_thumb = None
    book_author = None

    title = None
    content = None

    def __init__(self, title=None, content=None):
        if title:
            self.title = title
        if content:
            self.content = content

    def set_book_title(self, title):
        self.book_title = title

    def set_book_thumb(self, thumb):
        self.book_thumb = thumb

    def set_book_author(self, author):
        self.book_author = author

    def set_title(self, title):
        self.title = title

    def set_content(self, content):
        self.content = content
