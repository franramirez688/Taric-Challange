from PyQt4 import QtGui
from taric_challange.gui.widgets.books_table import BooksTableWidget
from taric_challange.core.books_manager import BooksManager
from taric_challange.gui.widgets.books_list import BooksListWidget
from PyQt4 import QtCore
from taric_challange.gui.widgets.books_searcher import BooksSearcherWidget
from taric_challange.gui.icons import MAIN_WINDOW_ICON


class ISBNSearcherGUI(QtGui.QMainWindow):
    """ This class create a ISBN searcher window  """
    def __init__(self):
        super(ISBNSearcherGUI, self).__init__()
        self.setWindowTitle("ISBN Searcher")  # set window title
        self.setWindowIcon(QtGui.QIcon(MAIN_WINDOW_ICON))

        # Create a BooksManager instance
        self.books_manager = BooksManager()

        # Create the main layout
        self.create_main_layout()

    def create_main_layout(self):
        """ Create the main layout """
        # Create widgets
        self.books_searcher_widget = BooksSearcherWidget("ISBNdb searcher")
        self.books_list_widget = BooksListWidget("Founded results...")
        self.books_table_widget = BooksTableWidget("Item selected book details")

        # Create a menu bar
        self.create_menu_bar()

        # Create layout to hold the widgets
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.addWidget(self.books_searcher_widget)
        self.main_layout.addWidget(self.books_list_widget)
        self.main_layout.addWidget(self.books_table_widget)

        # Create a widget to display our final layout
        self.isbn_searcher_widget = QtGui.QWidget()
        self.isbn_searcher_widget.setLayout(self.main_layout)

        # Change global settings to display the window
        self.resize(850, 500)
        self.focus()  # focus to center of the active window
        self.statusBar().showMessage('Ready', 1500)  # create a status bar
        self.setCentralWidget(self.isbn_searcher_widget)

        # connections
        self.books_searcher_widget.book_searcher_line_edit.returnPressed.connect(self.update_books_list)
        self.books_searcher_widget.book_search_button.clicked.connect(self.update_books_list)
        self.books_list_widget.books_list.clicked.connect(self.update_table_list)

    def create_menu_bar(self):
        show_help_action = QtGui.QAction(QtGui.QIcon('exit.png'), '&Help', self)
        show_help_action.setShortcut('Ctrl+H')
        show_help_action.setStatusTip('Help information')
        show_help_action.triggered.connect(self.show_help_info)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Help')
        fileMenu.addAction(show_help_action)

    def show_help_info(self):
        QtGui.QMessageBox.information(self, "Search box", "Enter any word to search")

    def update_books_list(self):
        keyword = self.books_searcher_widget.get_text()
        if keyword is None or keyword == '':
            QtGui.QMessageBox.information(self, "Search box", "Enter any word to search")
        else:
            self.statusBar().showMessage('Searching on ISBNdb database...')
            try:
                self.books_manager.update_books(keyword)
            except Exception as exc:
                QtGui.QMessageBox.warning(self, "Warning box", "An exception occurred: %s" % exc)
            self.statusBar().showMessage('Finished', 1500)
            self.books_list_widget.update_list(self.books_manager.books_titles)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def update_table_list(self, index):
        """ method to update the table book list """
        book = self.books_manager.books[index.row()]  # get book object
        self.books_table_widget.update_table(book)

    def focus(self):
        """ Focus the window to the center of the screen
            http://stackoverflow.com/questions/20243637/pyqt4-center-window-on-active-screen
        """
        frame_geometry = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        center_point = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())
