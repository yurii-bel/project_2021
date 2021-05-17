from PyQt5 import QtGui, QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit, QLabel, QComboBox
import test



class DisplayElements(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.test = 0
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)

        self.setGeometry(500, 200, 800, 600)
        self.setWindowTitle('TimeSoft')
        self.display_elements()

        self.act = test.Actions

        self.show()

    def display_elements(self):
        self.lbl_action = QLabel('Add action:') # Labels for user input block.
        self.lbl_comments = QLabel('Comments:')
        self.lbl_date = QLabel('Date:')
        self.lbl_duration = QLabel('Duration:')
        self.lbl_category = QLabel('Category:')

        self.lbl_action.move(510, 80) # Moving labels to the right locations.
        self.lbl_category.move(510, 120)
        self.lbl_duration.move(510, 160)
        self.lbl_date.move(510, 200)
        self.lbl_comments.move(510, 240)

        # self.qLe_add_action = QLineEdit(self) # Adding input types
        # self.qLe_add_action.move(570,80) # for corresponding labels.
        # self.qLe_add_action.resize(191,20)

        # self.cBox_category = QComboBox(self)
        # self.cBox_category.addItems(self.categories)
        # self.cBox_category.setEditable(True)

        # self.cBox_category.move(570, 120)
        #     # self.cBox_category.clicked.connect(self.get_values)

        # self.btn_save = QPushButton('Save', self)
        # self.btn_save.setObjectName('btn')
        # self.btn_save.setToolTip('This is a button')
        # self.btn_save.setStyleSheet('QPushButton {background-color: #4B0082; color: #fff;}')
        # self.btn_save.move(570, 340)

