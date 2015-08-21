from taric_challange.isbndb_api_client import ISBNdbApiClient
from taric_challange.books import Book
from taric_challange.tools import is_isbn_code


class BooksManager(object):
    """ This class manages the books data retrieving """

    def __init__(self):
        self._isbndb_api_client = ISBNdbApiClient(dev_key='UQ8OR4XB')
        # self._library_thing_api_client = LibraryThingApiClient()
        self.books_titles = {}

    def get_books_from_all_collections(self, keyword):
        all_data = self._remote_request_data(str(keyword))
        all_books_ids = []
        if all_data is None:
            raise Exception("Imposible to get any data from the keyword: %s" % keyword)
        # Clear old values from books
        self.books_titles = {}
        for data in all_data:
            print all_data
            for single_search in data:
                book_ids = single_search.get('book_ids')
                if book_ids is None:
                    _book_id = single_search.get('book_id')
                    if _book_id not in all_books_ids:
                        all_books_ids.append(_book_id)
                        _book = Book(single_search)
                        self.books_titles[_book.title] = _book
                elif book_ids:  # maybe, book_ids == []
                    for b_id in book_ids:
                        if b_id not in all_books_ids:
                            book_data = self._isbndb_api_client.request_data(book=b_id)[0][0]
                            if book_data:
                                _book = Book(book_data)
                                self.books_titles[_book.title] = _book

    def _remote_request_data(self, keyword):
        """ Get all the data from the requested keyword """
        fields = keyword.split(':')
        all_data = None
        print "keyword"
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
        elif is_isbn_code(keyword):
            print "keyword"
            all_data = self._isbndb_api_client.request_data(book=keyword)
            print all_data
        else:
            all_data = self._isbndb_api_client.request_data(all_collections=keyword, query=True)
        return all_data
