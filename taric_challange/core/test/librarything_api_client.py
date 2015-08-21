import unittest
from taric_challange.core.apis.librarything_api_client import LibraryThingApiClient


class LibraryThingApiClientTest(unittest.TestCase):

    def complete_test(self):
        api = LibraryThingApiClient()

        # Get cover thanks to ISBN code
        data = api.request_cover('0545010225')  # Harry Potter
        self.assertTrue(data is not None)
