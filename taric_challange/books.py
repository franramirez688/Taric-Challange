from taric_challange.library_thing_api_client import LibraryThingApiClient


class Book(object):
    """ Class to model a Book object """

    def __init__(self, data):
        self._data = data

    @property
    def title(self):
        return self._data.get('title', '-')

    @property
    def publisher(self):
        return self._data.get('publisher_name', '-')

    @property
    def language(self):
        return self._data.get('language', '-')

    @property
    def subjects(self):
        subjects = self._data.get('subject_ids')
        valid_subjects = []
        if subjects:
            for s in subjects:
                s = s.replace('_', ' ')
                s = s.capitalize()
                valid_subjects.append(s)
        return '\n'.join(valid_subjects)

    @property
    def author(self):
        author_data = self._data.get('author_data')
        author_name = '-'
        if author_data:
            author_name = author_data[0].get("name", '-')
        return author_name

    @property
    def isbn10(self):
        return self._data.get('isbn10', '-')

    @property
    def isbn13(self):
        return self._data.get('isbn13', '-')

    @property
    def edition(self):
        return self._data.get('edition_info', '-')

    @property
    def cover(self):
        isbn = self.isbn10 or self.isbn13
        cover_data = LibraryThingApiClient('73b0375ac4f292d859e4901a84d7d92d').request_cover(isbn)
        return cover_data
