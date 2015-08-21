from PyQt4.Qt import QTableWidget, QTableWidgetItem, QWidget, QLabel,\
    QVBoxLayout, QImage, QPixmap
from taric_challange.books import Book


MAIN_TABLE_DETAILS_BOOK = ["cover", "title", "author", "language", "publisher",
                           "subjects", "edition", "isbn10"]


class _CoverBookImageWidget(QLabel):
    """ Private class to create the cover book image widget """
    def __init__(self, cover_data):
        super(_CoverBookImageWidget, self).__init__()
        # Create a QImage object a load the cover data
        self.image = QImage()
        self.image.loadFromData(cover_data)

        # Associate the image to a Pixmap
        self.setPixmap(QPixmap(self.image))


class BooksTableWidget(QWidget):
    """ This class shows all the books results an their details """

    def __init__(self, label):
        super(BooksTableWidget, self).__init__()
        # init label and table widgets
        self.title_label = QLabel(label)
        self.books_table = QTableWidget()

        # Setting rows and columns number
        self.books_table.setRowCount(1)
        self.books_table.setColumnCount(len(MAIN_TABLE_DETAILS_BOOK))

        # Naming column labels
        self.books_table.setHorizontalHeaderLabels(MAIN_TABLE_DETAILS_BOOK)

        # Create the box layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.books_table)

        # set the final layout
        self.setLayout(self.main_layout)

    def update_table(self, book):
        assert isinstance(book, Book)
        # Fill the table with each book data
        for column, detail in enumerate(MAIN_TABLE_DETAILS_BOOK):
            detail_value = getattr(book, detail)
            if detail == 'cover':
                self.books_table.setCellWidget(0, column, _CoverBookImageWidget(detail_value))
            else:
                self.books_table.setItem(0, column, QTableWidgetItem(detail_value))

        # Resize all the Contents
        self.books_table.resizeColumnsToContents()
        self.books_table.resizeRowsToContents()
