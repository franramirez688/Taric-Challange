from taric_challange.core.apis.isbndb_api_client import ISBNdbApiClient
from taric_challange.core.models.book import Book
from taric_challange.core.tools import is_isbn_code
from taric_challange.core.exceptions import TaricGeneralException


COLLECTIONS = ['author', 'book', 'publisher', 'subject']
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
            raise TaricGeneralException("Impossible to get any data from the keyword: %s" % keyword)

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

        def _calculate_kwargs(keyword):
            """ Check if the keyword is like:
                book: Harry Potter && query: True && index: author_name
            """
            kwargs = {}
            queries = keyword.split('&&')
            for query in queries:
                fields = query.split(':')
                # If keyword is like, "subject: maths", etc.
                if len(fields) == 2:
                    _collection = fields[0].lower().strip()
                    _keyword = fields[1].strip()
                    if _collection in COLLECTIONS or _collection in QUERIES:
                        kwargs[_collection] = _keyword
                    else:
                        raise TaricGeneralException("This collection or query does not exist %s" %
                                                    _collection)
            _q = kwargs.get('query')
            if _q:
                if _q == 'True' or _q == 'true':
                    kwargs['query'] = True
                else:
                    kwargs['query'] = False
            return kwargs

        kwargs = _calculate_kwargs(keyword)
        if kwargs:
                all_data = self._isbndb_api_client.request_data(**kwargs)
        elif is_isbn_code(keyword):  # Check first is a ISBN code to make a fast request
            all_data = self._isbndb_api_client.request_data(book=keyword)
        else:  # else search around all the collections
            all_data = self._isbndb_api_client.request_data(all_collections=keyword, query=True)
        return all_data
