#! /usr/bin/env python

import sys
from PyQt4.QtGui import QApplication
from taric_challange.gui.isbn_searcher_main_window import ISBNSearcherGUI


def main():
    app = QApplication(sys.argv)  # create a new application
    isbn_searcher = ISBNSearcherGUI()  # create new instance of main window
    isbn_searcher.show()  # make instance visible
    isbn_searcher.raise_()  # raise instance to top of window stack
    sys.exit(app.exec_())  # monitor application for events

if __name__ == "__main__":
    main()
