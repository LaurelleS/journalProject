from genre import *


class Book:
    """
    A class that represents a book note
    """
    BOOK_INDEX = -1

    def __init__(self, title: str, notes: str, genre: Genre):
        self.__title = title
        self.__notes = notes
        self.__type = genre
        Book.BOOK_INDEX += 1

    def get_title(self):
        return self.__title

    def get_notes(self):
        return self.__notes

    def get_genre(self):
        return self.__type

    def __str__(self):
        return f'{self.__title}, {self.__notes}, {self.__type.name}'
