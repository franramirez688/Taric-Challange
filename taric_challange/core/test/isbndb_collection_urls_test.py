import unittest
from taric_challange.core.apis.isbndb_collection_urls import ISBNdbCollectionURLs
from taric_challange.core.environment import ISBNDB_API_V2_URL
from taric_challange.core.exceptions import TaricGeneralException


class ISBNdbCollectionURLsTest(unittest.TestCase):

    def complete_query_test(self):
        collection_urls = ISBNdbCollectionURLs('%s/json/%s' % (ISBNDB_API_V2_URL, "FAKEKEY"),
                                               book="Python is pretty",
                                               publisher="Fake Press",
                                               author="Guido van Rossum",
                                               subject="programming",
                                               query=True,
                                               index="author_name",)
        urls = collection_urls.urls
        expected_urls = ['http://isbndb.com/api/v2/json/FAKEKEY/books?q=python_is_pretty&i=author_name',
                         'http://isbndb.com/api/v2/json/FAKEKEY/authors?q=guido_van_rossum',
                         'http://isbndb.com/api/v2/json/FAKEKEY/publishers?q=fake_press',
                         'http://isbndb.com/api/v2/json/FAKEKEY/subjects?q=programming']
        self.assertEqual(urls, expected_urls)

    def complete_without_query_test(self):
        collection_urls = ISBNdbCollectionURLs('%s/json/%s' % (ISBNDB_API_V2_URL, "FAKEKEY"),
                                               book="Python is pretty",
                                               publisher="Fake Press",
                                               author="Guido van Rossum",
                                               subject="programming",
                                               index="author_name",)
        urls = collection_urls.urls
        expected_urls = ['http://isbndb.com/api/v2/json/FAKEKEY/book/python_is_pretty',
                         'http://isbndb.com/api/v2/json/FAKEKEY/author/guido_van_rossum',
                         'http://isbndb.com/api/v2/json/FAKEKEY/publisher/fake_press',
                         'http://isbndb.com/api/v2/json/FAKEKEY/subject/programming']
        self.assertEqual(urls, expected_urls)

    def all_collections_test(self):
        collection_urls = ISBNdbCollectionURLs('%s/json/%s' % (ISBNDB_API_V2_URL, "FAKEKEY"),
                                               all_collections="python",)
        urls = collection_urls.urls
        expected_urls = ['http://isbndb.com/api/v2/json/FAKEKEY/books?q=python',
                         'http://isbndb.com/api/v2/json/FAKEKEY/subjects?q=python',
                         'http://isbndb.com/api/v2/json/FAKEKEY/publishers?q=python',
                         'http://isbndb.com/api/v2/json/FAKEKEY/authors?q=python']

        self.assertEqual(urls, expected_urls)

    def bad_index_test(self):
        collection_urls = ISBNdbCollectionURLs('%s/json/%s' % (ISBNDB_API_V2_URL, "FAKEKEY"),
                                               book="Python is pretty",
                                               query=True,
                                               index="fake_index",)
        with self.assertRaises(TaricGeneralException):
            collection_urls.book_url
