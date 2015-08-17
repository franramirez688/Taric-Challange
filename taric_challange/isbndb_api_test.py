import unittest
from taric_challange.isbndb_api import ISBNdbApiClient


class ISBNdbApiTest(unittest.TestCase):

    def complete_test(self):
        api = ISBNdbApiClient(dev_key='GJXKT30B')

        # Get books by ISBN number
        print api.get_data(isbn='0444002383')

        # Get books by title
        print api.get_data(title='harry potter')

        # Get books by publisher
        print api.get_data(author='Richards Rowland')

        # Get books by subject
        print api.get_data(subject='numerical_analysis_data_processing')
