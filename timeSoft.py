from sqlite3.dbapi2 import Time
import sys

sys.path.append(".")

from PyQt5 import QtGui, QtWidgets, uic

# from logic.actions_ui import ActionsUI
from logic.time_db import TimeDb
from logic.time_add_activity import ActionsUI



class MainUI(QtWidgets.QMainWindow):
    '''
    This class implements Main Window of TimeSoft program.
    '''
    def __init__(self):
        super().__init__()
        self.timedb = TimeDb('database\\yurii_bel\\time_db.db')

        # Loading UI interfaces.
        self.mUi = uic.loadUi('design\\MainWindow.ui')  # Main window ui.
        # self.aUi = ActionsUI  # Loading ActionsUI class from logic.
        self.rUi = uic.loadUi('design\\register.ui')  # Registration window ui.
        self.lUi = uic.loadUi('design\\login.ui')  # Login window ui.
        self.sUi = uic.loadUi('design\\settings.ui')  # Settings window ui.
        self.wUi = self.mUi.viewWidget

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
        
        self.table()

        self.mUi.show()

    def add_action(self):
        '''
        Current method shows user interface action adding.
        '''
        self.aUi = ActionsUI()  # Loading ActionsUI class from logic.

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

    def table(self):
        lay = QtWidgets.QVBoxLayout()

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setRowCount(2)
        self.table.resizeColumnsToContents()

        act_name = QtWidgets.QTableWidgetItem('Название события')
        self.table.setHorizontalHeaderItem(0, act_name)
        act_category = QtWidgets.QTableWidgetItem('Категория')
        self.table.setHorizontalHeaderItem(1, act_category)
        act_duration_time = QtWidgets.QTableWidgetItem('Длительность')
        self.table.setHorizontalHeaderItem(2, act_duration_time)
        act_user_date = QtWidgets.QTableWidgetItem('Дата создания')
        self.table.setHorizontalHeaderItem(3, act_user_date)
        act_comment = QtWidgets.QTableWidgetItem('Комментарий')
        self.table.setHorizontalHeaderItem(4, act_comment)

        name = QtWidgets.QTableWidgetItem(\
            self.timedb.custom_sql(f'SELECT act_name FROM Activity \
                WHERE user_id = 43'))
        self.table.setItem(0, 0, name)

        lay.addWidget(self.table)
        self.wUi.setLayout(lay)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainUI()
    sys.exit(app.exec())
