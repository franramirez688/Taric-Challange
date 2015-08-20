import requests
from taric_challange.exceptions import RequestErrorException, GeneralException
import json
import re
from taric_challange.tools import is_isbn_code
from taric_challange.environment import get_isbndb_api_key, ISBNDB_API_V2_URL
from requests.exceptions import RequestException, ConnectionError, Timeout


VALID_INDEX_VALUES = ["author_id",  # (ISBNdb's internal author_id)
                      "author_name",
                      "publisher_id",  # (ISBNdb's internal publisher_id)
                      "publisher_name",
                      "book_summary",
                      "book_notes",
                      "dewey",  # (dewey decimal number)
                      "lcc",  # (library of congress number)
                      "combined",  # (searches across title, author name and publisher name)
                      "full"]  # (searches across all indexes)


class CollectionURLs(object):
    """ It helps to make easier the calculate of the different URLs depending
        on the collection requested
    """
    white_space_pattern = re.compile(r'\s+')

    def __init__(self, remote_url, **kwargs):
        self._remote_url = remote_url

        # all_collections keyword is similar to make a big query with all the existing collections
        self._all_collections = self._validate_collection_name(kwargs.get('all_collections'))

        self._book_name = self._all_collections or self._validate_collection_name(kwargs.get('book'))
        self._author_name = self._all_collections or self._validate_collection_name(kwargs.get('author'))
        self._subject_name = self._all_collections or self._validate_collection_name(kwargs.get('subject'))
        self._publisher_name = self._all_collections or self._validate_collection_name(kwargs.get('publisher'))

        self._query = True if self._all_collections else kwargs.get('query', False)
        self._index = kwargs.get('index')

    def _validate_collection_name(self, collection):
        """  Change white spaces to underscores and upper case to lower case
        """
        if collection is None:
            return
        c = self.white_space_pattern.sub('_', collection)
        # check is collection is not a ISBN number, like 084930315X
        if not is_isbn_code(c):
            c = c.lower()  # Change it to lower case
        return c

    def _get_valid_url(self, _request, collection):
        """ Select a valid URL depending on if user uses a query or not.
            Format:
                without query: http://isbndb.com/api/v2/json/[your-api-key]/book/084930315X
                with query: http://isbndb.com/api/v2/json/[your-api-key]/books?q=science
        """
        if self._query:
            valid_url = "%s/%ss?q=%s" % (self._remote_url, _request, collection)
        else:
            valid_url = "%s/%s/%s" % (self._remote_url, _request, collection)
        return valid_url

    @property
    def book_url(self):
        """ Get book collection URL """
        if self._book_name:
            url = self._get_valid_url("book", self._book_name)
            # If index exists and is valid, we have to add another query
            if self._query and self._index:
                if self._index in VALID_INDEX_VALUES:
                    url = '%s&i=%s' % (url, self._index)
                else:
                    raise GeneralException("Invalid index: %s. Please enter a valid option:\n"
                                           "%s" % (self._index, '\n'.join(VALID_INDEX_VALUES)))
            return url

    @property
    def subject_url(self):
        """ Get subject collection URL """
        if self._subject_name:
            url = self._get_valid_url("subject", self._subject_name)
            return url

    @property
    def publisher_url(self):
        """ Get publisher collection URL """
        if self._publisher_name:
            url = self._get_valid_url("publisher", self._publisher_name)
            return url

    @property
    def author_url(self):
        """ Get author collection URL """
        if self._author_name:
            url = self._get_valid_url("author", self._author_name)
            return url

    @property
    def urls(self):
        """ Return all the valid API Collections URLs """
        urls = []
        if self._all_collections:
            urls = [self.book_url, self.subject_url, self.publisher_url, self.author_url]
        else:
            if self._book_name:
                urls.append(self.book_url)
            if self._author_name:
                urls.append(self.author_url)
            if self._publisher_name:
                urls.append(self.publisher_url)
            if self._subject_name:
                urls.append(self.subject_url)
        return [_url for _url in urls if _url is not None]


class ISBNdbApiClient(object):
    ''' This class get all the information about any book thanks to API v2 from ISBNdb.com '''

    def __init__(self, dev_key=None):
        self._dev_key = dev_key or get_isbndb_api_key()
        self._remote_url = '%s/json/%s' % (ISBNDB_API_V2_URL, self._dev_key)

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
        collection_urls = CollectionURLs(self._remote_url, **kwargs)
        urls = collection_urls.urls

        # Handling possible exceptions
        try:
            responses = [requests.get(url=url) for url in urls]
        except ConnectionError:
            raise RequestErrorException("A connection error occurred")
        except Timeout:
            raise RequestErrorException("The request timed out")
        except RequestException as exc:
            raise RequestErrorException("An error occurred while handling your request\n%s" % exc)
        except Exception as exc:
            raise RequestErrorException(str(exc))

        return responses

    def request_data(self, **kwargs):
        """ return a list of data """
        responses = self.request(**kwargs)
        data = [self.deserialize(response).get('data') for response in responses]
        return data

    def deserialize(self, response):
        """ deserialize the response content using JSON format """
        if response.status_code != 200:
            raise RequestErrorException(response.status_code)(response.content)
        return json.loads(response.content)
