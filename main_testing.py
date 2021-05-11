import sys
import uuid
import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTime, QDate
from PyQt5 import QtCore, QtGui, QtWidgets

from design.MainWindow import Ui_MainWindow  # importing main UI

from addding_editing_actions_ui import ActionUI  
from testing.actions_ui_test.edit import Ui_Form  


class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setUi()

    def setUi(self):
        self.mUi = Ui_MainWindow()  # Main GUI class
        self.mUi.setupUi(self)

        self.addAction = ActionUI()
        print(self.mUi.btn_add_event)
        self.mUi.btn_add_event.clicked.connect(self.open_add_action_window)
        
    def open_add_action_window(self):
        self.addAction.show()
    


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainUI()
    win.show()
    sys.exit(app.exec())