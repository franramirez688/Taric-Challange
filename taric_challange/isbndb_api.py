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


class ISBNdbApiClient(object):
    ''' This class get all the information about any book thanks to API v2 from ISBNdb.com '''
    white_space_pattern = re.compile(r'\s+')

    def __init__(self, dev_key=None):
        self._dev_key = dev_key or get_dev_key()
        self._remote_url = '%s/json/%s' % (API_V2_URL, self._dev_key)

    def get_data(self, **kwargs):
        """ Get the result of searching any book using the ISBNdb API v2

            title = 
            isbn = 
            author = 
            subject = 
            publisher = 
            query = True or False
            index = author_id, book_notes, etc

        Return a json object
        """
        if not kwargs:
            raise GeneralException("You must introduce any argument,"
                                   " title, ISBN, etc.")
        title = kwargs.get('title')
        isbn = kwargs.get('isbn')
        author = kwargs.get('author')
        subject = kwargs.get('subject')
        publisher = kwargs.get('publisher')
        query = kwargs.get('query')
        index = kwargs.get('index')

        if title:
            if query:
                url = "%s/books?q=%s" % (self._remote_url, self.validate_arg(title))
                if index:
                    if index in VALID_INDEX_VALUES:
                        url = '%s&i=%s' % (url, index)
            else:
                url = "%s/book/%s" % (self._remote_url, self.validate_arg(title))
            response = requests.get(url=url)
        elif isbn:
            url = "%s/book/%s" % (self._remote_url, isbn)
            response = requests.get(url=url)
        elif author:
            url = "%s/author/%s" % (self._remote_url, self.validate_arg(author))
            response = requests.get(url=url)
        elif subject:
            url = "%s/subject/%s" % (self._remote_url, self.validate_arg(subject))
            response = requests.get(url=url)
        elif publisher:
            url = "%s/publisher/%s" % (self._remote_url, self.validate_arg(publisher))
            response = requests.get(url=url)

        data = self.desearilize(response).get('data')
        return data

    def validate_arg(self, arg):
        """  Change white spaces to underscores and change upper case to lower one
        """
        arg = self.white_space_pattern.sub('_', arg)
        return arg.lower()

    def desearilize(self, response):
        if response.status_code != 200:
            raise RequestErrorException(response.status_code)(response.content)
        return json.loads(response.content)

queries = '''author_id (ISBNdb's internal author_id)
author_name
publisher_id (ISBNdb's internal publisher_id)
publisher_name
book_summary
book_notes
dewey (dewey decimal number)
lcc (library of congress number)
combined (searches across title, author name and publisher name)
full (searches across all indexes)
'''
