import unittest
from taric_challange.isbndb_api_client import ISBNdbApiClient


class ISBNdbApiTest(unittest.TestCase):

    def complete_test(self):
        api = ISBNdbApiClient(dev_key='GJXKT30B')

        # Get books by ISBN number
        print api.request_data(book='0444002383')

        # Get books by ISBN number
        print api.request_data(book="pulp", query=True)

        # Get books by ISBN number
        print api.request_data(book="pulp", query=True, index="book_summary")

        # Get books by title
        print api.request_data(book='harry potter')

        # Get books by publisher
        print api.request_data(author='Richards Rowland')

        # Get books by subject
        print api.request_data(subject='numerical_analysis_data_processing')
