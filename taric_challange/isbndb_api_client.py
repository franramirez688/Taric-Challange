import requests
from taric_challange.exceptions import RequestErrorException, GeneralException
import json
import re
import os


API_V2_URL = 'http://isbndb.com/api/v2'
VALID_INDEX_VALUES = ["author_id",  # (ISBNdb's internal author_id)
                      "author_name",
                      "publisher_id",  # (ISBNdb's internal publisher_id)
                      "publisher_name",
                      "book_summary",
                      "book_notes",
                      "dewey",  # (dewey decimal number)
                      "lcc",  # (library of congress number)
                      "combined",  # (searches across title, author name and publisher name)
                      "full",  # (searches across all indexes)
                      ]


def get_dev_key():
    dev_key = os.getenv("ISBNDB_API_DEV_KEY")
    if dev_key is None:
        raise GeneralException("No developer key founded. Please, set your API key:\n"
                               "$> export ISBNDB_API_DEV_KEY=XXXXXXX")
    return dev_key


class CollectionsURLs(object):
    """ It helps to make easier the calculate of the different URLs depending
        on the collection requested
    """

    def __init__(self, remote_url, **kwargs):
        self._remote_url = remote_url

        self._all_collections = kwargs.get('all_collections')
        self._book_name = self.validate_collection_request(kwargs.get('book'))
        self._author_name = self.validate_collection_request(kwargs.get('author'))
        self._subject_name = self.validate_collection_request(kwargs.get('subject'))
        self._publisher_name = self.validate_collection_request(kwargs.get('publisher'))

        self._query = kwargs.get('query')
        self._index = kwargs.get('index')

        # Calling to requested methods
        # TODO: ALL URLS

    def get_valid_url(self, _request, collection):
        """ Select a valid URL depending on if user uses a query """
        if self._query:
            valid_url = "%s/%ss?q=%s" % (self._remote_url, _request, collection)
        else:
            valid_url = "%s/%s/%s" % (self._remote_url, _request, collection)
        return valid_url

    @property
    def book(self):
        url = self.get_valid_url("book", self._book_name)
        # If index exists and is valid, we have to add another query
        if self._query and self._index:
            if self.index in VALID_INDEX_VALUES:
                url = '%s&i=%s' % (url, self._index)
            else:
                raise GeneralException("Invalid index: %s. Please enter a "
                                       "valid option:\n%s" % (self._index, '\n'.join(VALID_INDEX_VALUES)))
        return url

    @property
    def subject(self):
        url = self.get_valid_url("subject", self._subject_name)
        return url

    @property
    def publisher(self):
        url = self.get_valid_url("publisher", self._publisher_name)
        return url

    @property
    def author(self):
        url = self.get_valid_url("author", self._author_name)
        return url

    @property
    def all_collections(self):
        urls = [self.book, self.subject, self.publisher, self.author]
        return urls


class ISBNdbApiClient(object):
    ''' This class get all the information about any book thanks to API v2 from ISBNdb.com '''
    white_space_pattern = re.compile(r'\s+')

    def __init__(self, dev_key=None):
        self._dev_key = dev_key or get_dev_key()
        self._remote_url = '%s/json/%s' % (API_V2_URL, self._dev_key)

    def request(self, **kwargs):
        """ Get the result of searching any book using the ISBNdb API v2

            title = book's title
            isbn = book's ISBN number (ISBN10 or ISBN13)
            author = author's name
            subject = book's subject
            publisher = book's publisher
            query = True or False
            index = author_id, book_notes, etc

        Return a json object
        """
        if not kwargs:
            raise GeneralException("You must introduce any argument,"
                                   " title, ISBN, etc.")
        urls = CollectionsURLs(self._remote_url, **kwargs)
        responses = [requests.get(url=url) for url in urls]
        return responses

    def request_data(self, **kwargs):
        """ return a list of data """
        responses = self.request(**kwargs)
        data = [self.deserialize(response).get('data') for response in responses]
        return data

    def validate_collection_request(self, collection):
        """  Change white spaces to underscores and upper case to lower case
        """
        if collection is not None:
            c = self.white_space_pattern.sub('_', collection)
            # check is collection is not a ISBN number, like 084930315X
            if c != collection:
                c = c.lower()  # Change it to lower case
            return c

    def deserialize(self, response):
        """ deserialize the response content using JSON format """
        if response.status_code != 200:
            raise RequestErrorException(response.status_code)(response.content)
        return json.loads(response.content)

    def handle_urls_selector(self, **kwargs):
        """ Get a valid URL depending on the arguments """
        all_collections = kwargs.get('all_collections')
        if all_collections:
            book = author = subject = publisher = all_collections
        else:
            book = self.validate_collection_request(kwargs.get('book'))
            author = self.validate_collection_request(kwargs.get('author'))
            subject = self.validate_collection_request(kwargs.get('subject'))
            publisher = self.validate_collection_request(kwargs.get('publisher'))
        query = kwargs.get('query')
        index = kwargs.get('index')

        def _url(_request, collection):
            """ Select a valid URL depending on if user uses a query """
            if query:
                valid_url = "%s/%ss?q=%s" % (self._remote_url, _request, collection)
            else:
                valid_url = "%s/%s/%s" % (self._remote_url, _request, collection)
            return valid_url

        urls = []
        if book:
            url = _url("book", book)
            # If index exists and is valid, we have to add another query
            if query and index:
                if index in VALID_INDEX_VALUES:
                    url = '%s&i=%s' % (url, index)
                else:
                    raise GeneralException("Invalid index: %s. Please enter a "
                                           "valid option:\n%s" % (index,
                                                                  '\n'.join(VALID_INDEX_VALUES)))
            urls.append(url)
        if author:
            urls.append(_url("author", author))
        if subject:
            urls.append(_url("subject", subject))
        if publisher:
            urls.append(_url("publisher", publisher))
        return urls
