import unittest
from taric_challange.core.apis.isbndb_api_client import ISBNdbApiClient


class ISBNdbApiClientTest(unittest.TestCase):

    def complete_test(self):
        api = ISBNdbApiClient()

        # Get books by ISBN number
        data = api.request_data(book='0444002383')
        self.assertEqual(data[0][0].get("book_id"), 'numerical_analysis_for_computer_science')

        # Get books by title query and an index of the database
        data = api.request_data(book="harry potter", query=True, index="book_summary")
        good_request = False
        for each_search in data[0]:
            if each_search.get('book_id') == 'animales_fantasticos_y_donde_encontrarlos':
                good_request = True
        self.assertTrue(good_request)

        # Get books by subject
        data = api.request_data(subject='numerical_analysis_data_processing')
        self.assertIn('numerical_analysis_for_computer_science', data[0][0].get("book_ids"))
