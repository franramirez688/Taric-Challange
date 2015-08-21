from PyQt4.Qt import QMainWindow, QPushButton, QLineEdit, QLabel,\
    QHBoxLayout, QVBoxLayout, QWidget
from taric_challange.books_table_widget import BooksTableWidget
from taric_challange.books_manager import BooksManager
from taric_challange.books_list_widget import BooksListWidget
from PyQt4 import QtCore
from taric_challange.books_searcher_widget import BooksSearcherWidget


class ISBNSearcherGUI(QMainWindow):
    """ This class create a ISBN seracher window  """
    def __init__(self, parent=None):
        super(ISBNSearcherGUI, self).__init__()
        self.setWindowTitle("ISBN Searcher")  # set window title

        # Create a BooksManager instance
        self.books_manager = BooksManager()

        self.create_main_layout()

    def create_main_layout(self):

        # Create widgets
        self.books_searcher_widget = BooksSearcherWidget("ISBNdb searcher")
        self.books_list_widget = BooksListWidget("Founded results...")
        self.books_table_widget = BooksTableWidget("Item selected book details")

        # Create layout to hold the widgets
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.books_searcher_widget)
        self.main_layout.addWidget(self.books_list_widget)
        self.main_layout.addWidget(self.books_table_widget)

        # Create a widget to display our final layout
        self.isbn_searcher_widget = QWidget()
        self.isbn_searcher_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.isbn_searcher_widget)

        # connections
        self.books_searcher_widget.book_search_button.clicked.connect(self.update_books_list)
        self.books_list_widget.books_list.doubleClicked.connect(self.update_table_list)

    def update_books_list(self):
        keyword = self.books_searcher_widget.get_text()
        if keyword is None or keyword == '':
            print "No hay boooookkkssss"
        else:
            self.books_manager.get_books_from_all_collections(keyword)
            self.books_list_widget.update_list(self.books_manager.books_titles.keys())

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def update_table_list(self, index):
        book_title_selected = index.data().toString()
        print "book_title_selected --_> %s" % book_title_selected
        book = self.books_manager.books_titles.get(str(book_title_selected))
        self.books_table_widget.update_table(book)
