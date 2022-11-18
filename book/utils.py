import logging
import json
from book.redis import RedisCode


class Cache:
    def __init__(self):
        self.cache = RedisCode()

    def get_book(self, user):
        """get book from memory"""
        try:
            books = self.cache.extract(str(user))
            if books is not None:
                return json.loads(books)
            return {}

        except Exception as e:
            logging.error(e)

    def add_book(self, user, book):
        """adding book to memory"""
        try:
            book_dict = self.get_book(user)
            book_dict.update({book.get('id'): book})
            self.cache.save(str(user), json.dumps(book_dict))
        except Exception as e:
            logging.error(e)

    def update_book(self, user, books):
        """delete book from memory"""
        book_id = str(books.get('id'))
        books_dict = self.get_book(user)
        book = books_dict.get(book_id)
        if book is not None:
            books_dict.update({book_id: books})
            self.cache.save(user, json.dumps(books_dict))

    def delete_note(self, user, id):
        """deleting the book from the memory"""
        try:
            book_dict = self.get_book(user)
            book_dict.pop(str(id))
            self.cache.save(str(user), json.dumps(book_dict))

        except Exception as error:
            logging.exception(error)
