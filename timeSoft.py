import sys

sys.path.append(".")

from PyQt5 import QtGui, QtWidgets, uic

from logic.actions_ui import ActionsUI


class MainUI(QtWidgets.QMainWindow):
    '''
    This class implements Main Window of TimeSoft program.
    '''
    def __init__(self):
        super().__init__()

        # Loading UI interfaces.
        self.mUi = uic.loadUi('design\\MainWindow.ui')  # Main window ui.
        self.aUi = ActionsUI()  # Loading ActionsUI class from logic.
        self.rUi = uic.loadUi('design\\register.ui')  # Registration window ui.
        self.lUi = uic.loadUi('design\\login.ui')  # Login window ui.
        self.sUi = uic.loadUi('design\\settings.ui')  # Settings window ui.

        # Connecting buttons to slots.
        # All commented stuff is not yet realized.
        self.mUi.btn_plus.clicked.connect(self.add_action)
        #self.mUi.btn_forecast.clicked.connect(self.forecasting)
        #self.mUi.btn_background.clicked.connect(self.change_theme)
        self.mUi.btn_settings.clicked.connect(self.settings)
        self.mUi.btn_exit.clicked.connect(self.mUi.close)
        
        # Setting pixmap for 'lbl_logoimg' element.
        logo = QtGui.QPixmap('design\\img\\icons\\Logo.png')
        self.mUi.lbl_logoimg.setPixmap(logo)

        self.mUi.show()

    def add_action(self):
        '''
        Current method shows user interface action adding.
        '''
        self.aUi.aUi.show()

    def settings(self):
        '''
        Current method shows user interface settings window.
        '''
        self.sUi.show()

    def login(self):
        '''
        Current method shows user interface login window.
        '''
        pass

    def registration(self):
        '''
        Current method shows user interface registration window.
        '''
        pass

    def visualize(self, object):
        '''
        Current method displays table/graph/chart view containing all actions. 
        '''
        pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainUI()
    sys.exit(app.exec())
