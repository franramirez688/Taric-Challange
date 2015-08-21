from PyQt4.Qt import QListView, QAbstractItemView, QStringListModel, QWidget,\
    QLabel, QVBoxLayout


class BooksListWidget(QWidget):
    """ Uneditable list's books """

    def __init__(self, label):
        super(BooksListWidget, self).__init__()

        # init label and table widgets
        self.title_label = QLabel(label)
        self.books_list = QListView()

        # List settings
        self.books_list.minimumHeight()

        # Make the list uneditable
        self.books_list.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Create a model for the list's books
        self.model = QStringListModel()

        # Apply the model to the list view
        self.books_list.setModel(self.model)

        # Create the layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.books_list)

        # Set the layout
        self.setLayout(self.main_layout)

    def update_list(self, books_list):
        """ Update the books list """
        assert isinstance(books_list, list)
        self.model.setStringList(books_list)
