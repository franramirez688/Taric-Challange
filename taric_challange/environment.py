import os
from taric_challange.exceptions import GeneralException


ISBNDB_API_V2_URL = 'http://isbndb.com/api/v2'
LIBRARYTHING_API_URL = 'http://covers.librarything.com/devkey'


def _get_dev_key(_key):
    dev_key = os.getenv(_key)
    if dev_key is None:
        raise GeneralException("No developer key founded. Please, set your API key:\n"
                               "$> export %s=XXXXXXX" % _key)
    return dev_key


def get_isbndb_api_key():
    return _get_dev_key(ISBNDB_API_V2_URL)


def get_librarything_api_key():
    return _get_dev_key(LIBRARYTHING_API_URL)
