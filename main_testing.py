import sys
import uuid
import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTime, QDate
from PyQt5 import QtCore, QtGui, QtWidgets

from design.MainWindow import Ui_MainWindow  # importing main UI

from logic.addding_editing_actions import Actions  
from testing.actions_ui_test.edit import Ui_Form  


class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.mUi = Ui_MainWindow()
        self.mUi.setupUi(self)

    def open_add_action_window(self):
        pass



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainUI()
    win.show()
    sys.exit(app.exec())