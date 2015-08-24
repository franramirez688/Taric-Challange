# ISBNdb Searcher

This is a PyQt application which is able to create requests to the website [ISBNdb](http://isbndb.com/) and get all the necessary information details in a simple table.

Moreover, it creates requests to another website named [LibraryThing](http://www.librarything.com/home) to get book's cover from each one of our requests.


**Note**: the ISBNdb API is the newest version (V2). See [ISBNdb API -- Version 2](http://isbndb.com/api/v2/docs)

## Platforms

It has been run only on `Ubuntu 15.04`


## Requirements

* [Python 2.7](https://www.python.org/download/releases/2.7/)
* [PyQt4](http://pyqt.sourceforge.net/Docs/PyQt4/installation.html)


## Up & Running

You need to create each Developer Key from the previous websites


* [ISBNdb Developer API Key](http://isbndb.com/api/v1/docs/keys)
* [LibraryThing Developer API Key](http://www.librarything.com/services/keys.php)

And set each one to these environment variables:

```sh
$ export ISBNDB_API_V2_KEY=XXXXXXXXXX
$ export LIBRARYTHING_API_KEY=XXXXXXXXXXX

```

Install the requirements python packages:

```sh
$ pip install -r requirements.txt
```

Finally, execute the **app.py** file to launch the application:

```sh
$ ./app.py
```

## Testing

Run the tests with `nose` package tool. Install the necessary packages

```sh
$ pip install -r ./taric_challange/core/test/requirements.txt
$ nosetests
```

## Searches

This is a brief explanation to use the ISBNdb searcher.

You can make searches about these collections: **book (title or isbn), author, subject or publisher**


### Simple and general search around all the possible collections

```
science fiction
```

`WARNING!` This search generates a lot of ones so you could spend all your free daily ISBNdb API requests

### A specific search

```
book: 0545010225
```

### A query search

```
subject: brain disease && query: True
```

### A query search with a customized index (only books and query must be True)

```
book: Harry Potter && query: True && index: author_name
```

**Note**: valid index values:

*   author_id -> ISBNdb's internal author_id
*   author_name
*   publisher_id -> ISBNdb's internal publisher_id
*   publisher_name
*   book_summary
*   book_notes
*   dewey -> dewey decimal number
*   lcc -> library of congress number
*   combined -> searches across title, author name and publisher name
*   full -> searches across all indexes
