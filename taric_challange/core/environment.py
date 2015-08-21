import os
from taric_challange.core.exceptions import TaricGeneralException


####### API URLS ########

ISBNDB_API_V2_URL = 'http://isbndb.com/api/v2'
LIBRARYTHING_API_URL = 'http://covers.librarything.com/devkey'


####### DEVELOPER API KEYS ########

ISBNDB_API_V2_KEY = ''
LIBRARYTHING_API_KEY = ''


def _get_dev_key(_key_name):
    dev_key = os.environ.get(_key_name)
    if dev_key is None:
        raise TaricGeneralException("No developer key founded. Please, set your API key:\n"
                                    "$> export %s=XXXXXXX" % _key_name)
    return dev_key


def get_isbndb_api_key():
    return _get_dev_key("ISBNDB_API_V2_KEY")


def get_librarything_api_key():
    return _get_dev_key("LIBRARYTHING_API_KEY")
