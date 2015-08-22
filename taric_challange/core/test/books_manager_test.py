import unittest
from taric_challange.core.books_manager import BooksManager
from taric_challange.core.models.book import Book
from mock import Mock
import mock


data = {"author_data" : [
        {
            "name": "Richards, Rowland",
            "id": "richards_rowland"
        }],
        "awards_text": "",
        "marc_enc_level": "4",
        "subject_ids": [
        "mechanics_applied",
        "physics"
        ],
        "summary": "",
        "isbn13": "9780849303159",
        "dewey_normal": "620.105",
        "title_latin": "Principles of solid mechanics",
        "publisher_id": "crc_press",
        "dewey_decimal": "620/.1/05",
        "publisher_text": "Boca Raton, FL : CRC Press, 2001.",
        "language": "eng",
        "physical_description_text": "446 p. : ill. ; 24 cm.",
        "isbn10": "084930315X",
        "edition_info": "(alk. paper)",
        "urls_text": "",
        "lcc_number": "TA350",
        "publisher_name": "CRC Press",
        "book_id": "principles_of_solid_mechanics",
        "notes": "Includes bibliographical references and index.",
        "title": "Principles of solid mechanics",
        "title_long": ""}


class BooksManagerTest(unittest.TestCase):

    def simple_local_test(self):
        manager = BooksManager()
        book = Book(data)

        manager._remote_request_data = Mock(return_value=[[data]])
        manager.update_books('fake keyword')

        self.assertEqual(book.title, manager.books_titles[0])
        self.assertEqual(book.publisher, manager.books[0].publisher)
        self.assertEqual(book.subjects, manager.books[0].subjects)
        self.assertEqual(book.author, manager.books[0].author)
        self.assertEqual(book.isbn10, manager.books[0].isbn10)
        self.assertEqual(book.isbn13, manager.books[0].isbn13)
        self.assertEqual(book.edition, manager.books[0].edition)
        self.assertEqual(book.language, manager.books[0].language)
