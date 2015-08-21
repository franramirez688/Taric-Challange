from taric_challange.core.environment import get_librarything_api_key,\
    LIBRARYTHING_API_URL
import requests
from taric_challange.core.exceptions import TaricRequestError
from requests.exceptions import RequestException, Timeout, ConnectionError


dev_key = '73b0375ac4f292d859e4901a84d7d92d'


class LibraryThingApiClient(object):
    """ This class create a request to LibraryThing API to get as response any cover book """

    def __init__(self, dev_key=None, size_cover='medium'):
        self._dev_key = dev_key or get_librarything_api_key()
        self._remote_url = '%s/%s/%s/isbn' % (LIBRARYTHING_API_URL, self._dev_key, size_cover)

    def request_cover(self, isbn):
        """ Return the image cover book data
            @param isbn: ISBN code (ISBN 10 or 13)
        """
        url = '%s/%s' % (self._remote_url, isbn)
        try:
            response = requests.get(url=url)
        except ConnectionError:
            raise TaricRequestError("A connection error occurred")
        except Timeout:
            raise TaricRequestError("The request timed out")
        except RequestException as exc:
            raise TaricRequestError("An error occurred while handling your request\n%s" % exc)
        except Exception as exc:
            raise TaricRequestError(str(exc))

        if response.status_code != 200:
            raise TaricRequestError(response.status_code)(response.content)
        return response.content
