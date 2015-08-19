#! /usr/bin/env python


import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import QMainWindow, QApplication


from radio_button_widget import RadioButtonWidget
from PyQt4.Qt import QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit,\
    QGridLayout, QStackedLayout

class Wheat: pass
class Potato: pass


class ISBNSearcher(QMainWindow):
    """ This class create a ISBN seracher window  """
    def __init__(self, parent=None):
        super(ISBNSearcher, self).__init__()
        self.setWindowTitle("ISBN searcher")  # set window title
        self.create_select_isbn_layout()

        self.stacked_layout = QStackedLayout()  # this holds the various layouts
        self.stacked_layout.addWidget(self.select_crop_widget)

        # set the central widget to display the layout
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)

    def create_select_isbn_layout(self):
        # this is the initial layout of the window
        self.crop_radio_buttons = RadioButtonWidget("ISBN ssearcher",
                                                    "Please select one",
                                                    ["wheat", "potato"])
        self.instantiate_button = QPushButton("Create a crop")

        # create a layout to hold the widgets
        self.initial_layout = QVBoxLayout()
        self.initial_layout.addWidget(self.crop_radio_buttons)
        self.initial_layout.addWidget(self.instantiate_button)

        self.select_crop_widget = QWidget()
        self.select_crop_widget.setLayout(self.initial_layout)

        #self.setCentralWidget(self.select_crop_widget)

        # connections
        self.instantiate_button.clicked.connect(self.instantiate_crop)

    def create_view_crop_layout(self, crop_type):
        # this is the second layout of the window - view 
        self.growth_label = QLabel("Growth")
        self.days_label = QLabel("Days Growing")
        self.status_label = QLabel("Crop Status")

        self.growth_line_edit = QLineEdit()
        self.days_line_edit = QLineEdit()
        self.status_line_edit = QLineEdit()

        self.manual_growth_button = QPushButton("Manually Grow")
        self.automatic_grow_button = QPushButton("Automatically Grow")

        self.grow_grid = QGridLayout()
        self.status_grid = QGridLayout()

        # add label widgets to the status layout
        self.status_grid.addWidget(self.growth_label, 0, 0)
        self.status_grid.addWidget(self.days_label, 1, 0)
        self.status_grid.addWidget(self.status_label, 2, 0)

        # add line edit widgets to the status layout
        self.status_grid.addWidget(self.growth_line_edit, 0, 1)
        self.status_grid.addWidget(self.days_line_edit, 1, 1)
        self.status_grid.addWidget(self.status_line_edit, 2, 1)

        # add widgets/layouts to the grow layout
        self.grow_grid.addLayout(self.status_grid, 0, 1)
        self.grow_grid.addWidget(self.manual_growth_button, 1, 0)
        self.grow_grid.addWidget(self.automatic_grow_button, 1, 1)

        # create a widget to display the grow layout
        self.view_crop_widget = QWidget()
        self.view_crop_widget.setLayout(self.grow_grid)

        # connections
        self.automatic_grow_button.clicked.connect(self.automatically_grow_crop)

    def instantiate_crop(self):
        crop_type = self.crop_radio_buttons.selected_button()
        if crop_type == 1:
            self.simulated_crop = Wheat()
        elif crop_type == 2:
            self.simulated_crop = Potato()

        self.create_view_crop_layout(crop_type)  # create the view crop growth layout
        self.stacked_layout.addWidget(self.view_crop_widget)  # add this to the stack
        self.stacked_layout.setCurrentIndex(1)  # change the visible layout in the stack


    def automatically_grow_crop(self):
        pass


def main():
    isbn_searcher_app = QApplication(sys.argv)  # create a new application
    isbn_searcher = ISBNSearcher()  # create new instance of main window
    isbn_searcher.show()  # make instance visible
    isbn_searcher.raise_()  # raise instance to top of window stack
    isbn_searcher_app.exec_()  # monitor application for events

if __name__ == "__main__":
    main()
