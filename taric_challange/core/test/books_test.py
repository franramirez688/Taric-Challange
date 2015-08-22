import unittest
from taric_challange.core.models.book import Book


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


class BookTest(unittest.TestCase):

    def book_model_test(self):
        book = Book(data)

        self.assertEqual(book.title, 'Principles of solid mechanics')
        self.assertEqual(book.publisher, 'CRC Press')
        self.assertEqual(book.subjects, 'Mechanics applied\nPhysics')
        self.assertEqual(book.author, "Richards, Rowland")
        self.assertEqual(book.isbn10, '084930315X')
        self.assertEqual(book.isbn13, '9780849303159')
        self.assertEqual(book.edition, '(alk. paper)')
        self.assertEqual(book.language, 'eng')
