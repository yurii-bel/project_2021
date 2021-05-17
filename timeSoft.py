import sys

sys.path.append(".")

from PyQt5 import QtGui, QtWidgets, uic

from logic.addding_editing_actions_ui import ActionsUI

class MainUI(QtWidgets.QMainWindow):
    '''
    This class implements Main Window of TimeSoft program.
    '''
    def __init__(self):
        super().__init__()

        # Loading UI's.
        self.mUi = uic.loadUi('design\\MainWindow.ui')
        self.aUi = ActionsUI()
        self.rUi = uic.loadUi('design\\register.ui')
        self.lUi = uic.loadUi('design\\login.ui')
        self.sUi = uic.loadUi('design\\settings.ui')

        # Connecting buttons to slots.
        # All commented stuff is not yet realized.
        self.mUi.btn_plus.clicked.connect(self.add_action)
        #self.mUi.btn_forecast.clicked.connect(self.forecasting)
        #self.mUi.btn_background.clicked.connect(self.change_theme)
        self.mUi.btn_settings.clicked.connect(self.settings)
        self.mUi.btn_exit.clicked.connect(self.mUi.close)
        
        # Setting pixmap for 'lbl_logoimg' element.
        _ = QtGui.QPixmap('design\\img\\icons\\Logo.png')
        self.mUi.lbl_logoimg.setPixmap(_)

        self.mUi.show()

    def add_action(self):
        self.aUi.aUi.show()

    def settings(self):
        self.sUi.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainUI()
    sys.exit(app.exec())
