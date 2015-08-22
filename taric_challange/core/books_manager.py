from taric_challange.core.apis.isbndb_api_client import ISBNdbApiClient
from taric_challange.core.models.book import Book
from taric_challange.core.tools import is_isbn_code
from taric_challange.core.exceptions import TaricGeneralException


COLLECTIONS = ['author', 'isbn', 'title', 'publisher', 'subject']
QUERIES = ['query', 'index']


class BooksManager(object):
    """ This class manages the books data retrieving """

    def __init__(self):
        self._isbndb_api_client = ISBNdbApiClient()
        self.books = []  # [("book_title": <Book object>),]
        self.books_titles = []

    def update_books(self, keyword):
        """ Update the books dictionary """
        all_data = self._remote_request_data(str(keyword))
        all_books_ids = []  # check if there is any repeated book_id
        if all_data is None:
            raise TaricGeneralException("Imposible to get any data from the keyword: %s" % keyword)

        # Clear old books data
        self.books = []
        self.books_titles = []

        # algorithm to calculate the Book objects
        for data in all_data:
            for single_search in data:
                # Search if data has a list of possible book_ids
                # else it would mean the data is a book_id data itself
                book_ids = single_search.get('book_ids')
                if book_ids is None:
                    _book_id = single_search.get('book_id')
                    if _book_id not in all_books_ids:
                        all_books_ids.append(_book_id)
                        _book = Book(single_search)
                        self.books.append(_book)
                        self.books_titles.append(_book.title)
                # Request with each single book_id from book_ids list
                elif book_ids:  # maybe, book_ids == []
                    for b_id in book_ids:
                        if b_id not in all_books_ids:
                            # Get the single book_id data
                            book_data = self._isbndb_api_client.request_data(book=b_id)[0][0]
                            if book_data:
                                _book = Book(book_data)
                                self.books.append(_book)
                                self.books_titles.append(_book.title)

    def _remote_request_data(self, keyword):
        """ Get all the data from the requested keyword
            You can make a keyword like this:
                author: Richard Rowland
                subject: mechanism
            A keyword without ':' key means that you want to use "all the collections"
            URL to search any book
        """
        fields = keyword.split(':')
        all_data = None
        # If keyword is like, "subject: maths"
        if len(fields) == 2:
            collection = fields[0].lower()
            keyword = fields[1].strip()
            if collection == 'title' or collection == 'isbn':
                all_data = self._isbndb_api_client.request_data(book=keyword, query=True)
            elif collection == 'author':
                all_data = self._isbndb_api_client.request_data(author=keyword, query=True)
            elif collection == 'publisher':
                all_data = self._isbndb_api_client.request_data(publisher=keyword, query=True)
            elif collection == 'subject':
                all_data = self._isbndb_api_client.request_data(subject=keyword, query=True)
        elif is_isbn_code(keyword):  # Check first is a ISBN code to make a fast request
            all_data = self._isbndb_api_client.request_data(book=keyword)
        else:  # else search around all the collections
            all_data = self._isbndb_api_client.request_data(all_collections=keyword, query=True)
        return all_data
