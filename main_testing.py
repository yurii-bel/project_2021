import sys
import uuid
import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTime, QDate
from PyQt5 import QtCore, QtGui, QtWidgets

from design.mainUI import MainWindow  # importing main UI
# from design.edit_event import Ui_Form  # importing edit_event UI

from addding_editing_actions_ui import ActionUI  # importing class that works
# with edit_event UI


class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.mUi = MainWindow  # Main GUI class
        #self.mUi.setupUi(self, self)

        self.aUi = ActionUI  # Add action GUI class

        # connect add event button from Main window to add event window
        self.mUi.btn_add_action.clicked.connect(self.open_add_action_window)
        
        self.aUi.btn_save.clicked.connect(self.save_action)
        
    def open_add_action_window(self):
        self.addActionUi.show()  

    def save_action(self):
        # spawning (creating) new objects in Main UI 
        self.lbl_action = QtWidgets.QLabel()
        self.lbl_action.setText('New action is here!')
        # self.lbl_action.setGeometry(400, 400, 100,)
        self.mUi.gridLayout.addWidget(self.lbl_action, 4, 3, 2, 2)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainUI()
    win.show()
    sys.exit(app.exec())