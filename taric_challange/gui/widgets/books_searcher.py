from PyQt4 import QtGui


class BooksSearcherWidget(QtGui.QWidget):

    def __init__(self, label):
        super(BooksSearcherWidget, self).__init__()

        # Create searcher widgets
        self.book_searcher_label = QtGui.QLabel(label)
        self.book_searcher_line_edit = QtGui.QLineEdit()
        self.book_search_button = QtGui.QPushButton("Search")

        # Create searcher layout
        self.book_searcher_box = QtGui.QHBoxLayout()
        self.book_searcher_box.addWidget(self.book_searcher_line_edit)
        self.book_searcher_box.addWidget(self.book_search_button)

        # Create main layout
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.addWidget(self.book_searcher_label)
        self.main_layout.addLayout(self.book_searcher_box)

        # Set the window layout
        self.setLayout(self.main_layout)

    def get_text(self):
        return self.book_searcher_line_edit.text()
