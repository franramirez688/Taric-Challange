import re


def is_isbn_code(keyword):
    if re.match('^[0-9]+', keyword):
        return True
    return False
