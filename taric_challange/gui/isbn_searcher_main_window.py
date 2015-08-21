from PyQt4.Qt import QMainWindow, QVBoxLayout, QWidget, QApplication,\
    QMessageBox
from taric_challange.gui.widgets.books_table import BooksTableWidget
from taric_challange.core.books_manager import BooksManager
from taric_challange.gui.widgets.books_list import BooksListWidget
from PyQt4 import QtCore
from taric_challange.gui.widgets.books_searcher import BooksSearcherWidget


class ISBNSearcherGUI(QMainWindow):
    """ This class create a ISBN searcher window  """
    def __init__(self, parent=None):
        super(ISBNSearcherGUI, self).__init__()
        self.setWindowTitle("ISBN Searcher")  # set window title

        # Create a BooksManager instance
        self.books_manager = BooksManager()

        self.create_main_layout()

    def create_main_layout(self):
        """ Create the main layout """
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

        # Change global settings to display the window
        self.resize(850, 500)
        self.focus()  # focus to center of the active window
        self.setCentralWidget(self.isbn_searcher_widget)

        # connections
        self.books_searcher_widget.book_searcher_line_edit.returnPressed.connect(self.update_books_list)
        self.books_searcher_widget.book_search_button.clicked.connect(self.update_books_list)
        self.books_list_widget.books_list.doubleClicked.connect(self.update_table_list)

    def update_books_list(self):
        keyword = self.books_searcher_widget.get_text()
        if keyword is None or keyword == '':
            QMessageBox.information(self, "Search box", "Enter any word to search")
        else:
            self.books_manager.update_books(keyword)
            self.books_list_widget.update_list(self.books_manager.books_titles)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def update_table_list(self, index):
        """ method to update the table book list """
        book = self.books_manager.books[index.row()][1]  # get book object
        self.books_table_widget.update_table(book)

    def focus(self):
        """ Focus the window to the center of the screen
            http://stackoverflow.com/questions/20243637/pyqt4-center-window-on-active-screen
        """
        frame_geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())
