from taric_challange.environment import get_librarything_api_key,\
    LIBRARYTHING_API_URL
import requests
from taric_challange.exceptions import RequestErrorException


dev_key = '73b0375ac4f292d859e4901a84d7d92d'


class LibraryThingApiClient(object):

    def __init__(self, dev_key=None, size_cover='medium'):
        self._dev_key = dev_key or get_librarything_api_key()
        self._remote_url = '%s/%s/%s/isbn' % (LIBRARYTHING_API_URL, self._dev_key, size_cover)

    def request_cover(self, isbn):
        url = '%s/%s' % (self._remote_url, isbn)
        response = requests.get(url=url)

        if response.status_code != 200:
            raise RequestErrorException(response.status_code)(response.content)
        return response.content
