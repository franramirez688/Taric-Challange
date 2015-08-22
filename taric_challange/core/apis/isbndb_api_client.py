import requests
from taric_challange.core.exceptions import TaricRequestError, TaricGeneralException
import json
from taric_challange.core.environment import get_isbndb_api_key, ISBNDB_API_V2_URL
from requests.exceptions import RequestException, ConnectionError, Timeout
from taric_challange.core.apis import ISBNdbCollectionURLs


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
            raise TaricGeneralException("You must introduce any argument,"
                                        " title, ISBN, etc.")
        collection_urls = ISBNdbCollectionURLs(self._remote_url, **kwargs)
        urls = collection_urls.urls

        # Handling possible exceptions
        try:
            responses = [requests.get(url=url) for url in urls]
        except ConnectionError:
            raise TaricRequestError("A connection error occurred")
        except Timeout:
            raise TaricRequestError("The request timed out")
        except RequestException as exc:
            raise TaricRequestError("An error occurred while handling your request\n%s" % exc)
        except Exception as exc:
            raise TaricRequestError(str(exc))

        return responses

    def request_data(self, **kwargs):
        """ return a list of data """
        responses = self.request(**kwargs)
        data = [self.deserialize(response).get('data') for response in responses]
        return data

    def deserialize(self, response):
        """ deserialize the response content using JSON format """
        if response.status_code != 200:
            TaricRequestError("Failed request, response status code: %s" % response.status_code)
        json_data = json.loads(response.content)
        error = json_data.get('error')
        if error:
            if error == "Daily request limit exceeded.":
                raise TaricRequestError("Change your Developer Key. "
                                        "Your daily request limit has been exceeded")
            else:
                raise TaricRequestError(error)
        return json_data
