from logic.actions_ui import ActionsUI
from logic.dblogic import DbLogic as db
from PyQt5 import QtGui, QtWidgets, uic
import sys
sys.path.append(".")


class MainUI(QtWidgets.QMainWindow):
    '''
    This class implements Main Window of TimeSoft program.
    '''

    def __init__(self):
        super().__init__()
        # Creating database instance.
        self.timedb = db

        # Creating variable for future storing name of user in it.
        self.user_n_name = None

        # Нужно автоматизировать разделителей (module os).
        # Loading UI interfaces.
        self.mUi = uic.loadUi('design\\MainWindow_d.ui') # Main window ui.
        self.aUi = ActionsUI() # Loading ActionsUI class from logic.
        self.rUi = uic.loadUi('design\\register_d.ui') # Registration window ui.
        self.lUi = uic.loadUi('design\\login_d.ui') # Login window ui.
        self.sUi = uic.loadUi('design\\settings_d.ui') # Settings window ui.
        self.tUi = uic.loadUi('design\\table.ui') # Table ui.
        self.wUi = self.mUi.viewWidget # Widget for viewing various data.

        # Connecting buttons to slots.
        # Main UI.
        self.mUi.mainwindow_btn_nav_add_act.clicked.connect(self.add_action)
        self.mUi.mainwindow_btn_settings.clicked.connect(self.settings)
        self.mUi.mainwindow_btn_exit.clicked.connect(self.mUi.close)

        # Login UI.
        self.lUi.login_btn_login.clicked.connect(self.login)
        self.lUi.login_btn_create_account.clicked.connect(
            self.show_registration)

        # Register UI.
        self.rUi.register_btn_login.clicked.connect(self.registration)
        self.rUi.register_btn_create.clicked.connect(self.show_login)

        # Settings UI.
        self.sUi.settings_btn_export.clicked.connect(self.settings_export)

        # When starting a program, first login UI appears.
        self.show_login()

    def show_login(self):
        '''
        Current method shows user interface login window.
        '''
        self.rUi.close()
        self.lUi.show()

    def login(self):
        self.db = self.timedb()
        login = self.lUi.login_lineedit_email.text()
        password = self.lUi.login_lineedit_password.text()

        self.db.login_user(login, password)

        if self.db.user_empty_name_bool == False:
            QtWidgets.QMessageBox.question(self, 'Ошибка!',
                                           self.db.user_empty_name_message, QtWidgets.QMessageBox.Ok)
        elif self.db.user_empty_password_bool == False:
            QtWidgets.QMessageBox.question(self, 'Ошибка!',
                                           self.db.user_empty_password_message, QtWidgets.QMessageBox.Ok)
        elif self.db.correct_login_info == False:
            QtWidgets.QMessageBox.question(self, 'Ошибка!',
                                           f'Неверный логин или пароль! ', QtWidgets.QMessageBox.Ok)

        elif self.db.correct_login_info == True:
            self.user_n_name = login
            self.lUi.close()
            self.mUi.show()
            self.view_table() # Viewing table.

    def show_registration(self):
        '''
        Current method shows user interface registration window.
        '''
        self.lUi.close()
        self.rUi.show()

    def registration(self):
        self.db = self.timedb()
        login = self.rUi.register_lineEdit_name.text()
        email = self.rUi.register_lineEdit_email.text()
        password = self.rUi.register_lineEdit_password.text()

        self.db.register_user(login, email, password)

        if self.db.user_exists_bool == False:
            QtWidgets.QMessageBox.question(self, 'Ошибка!',
                                           self.db.user_exists_message, QtWidgets.QMessageBox.Ok)
        elif self.db.user_email_bool == False:
            QtWidgets.QMessageBox.question(self, 'Ошибка!',
                                           self.db.user_email_message, QtWidgets.QMessageBox.Ok)
        elif self.db.user_empty_name_bool == False:
            QtWidgets.QMessageBox.question(self, 'Ошибка!',
                                           self.db.user_empty_name_message, QtWidgets.QMessageBox.Ok)
        elif self.db.user_empty_email_bool == False:
            QtWidgets.QMessageBox.question(self, 'Ошибка!',
                                           self.db.user_empty_email_message, QtWidgets.QMessageBox.Ok)
        elif self.db.user_empty_password_bool == False:
            QtWidgets.QMessageBox.question(self, 'Ошибка!',
                                           self.db.user_empty_password_message, QtWidgets.QMessageBox.Ok)
        elif self.db.user_incorrect_password_bool == False:
            QtWidgets.QMessageBox.question(self, 'Ошибка!',
                                           self.db.user_incorrect_password_message, QtWidgets.QMessageBox.Ok)
        else:
            self.rUi.close()
            self.lUi.show()

    def add_action(self):
        '''
        Current method shows user interface action adding.
        '''
        self.aUi.show_add_event()  # Loading ActionsUI class from logic.
        

    def visualize(self, object):
        '''
        Current method displays table/graph/chart view containing all actions. 
        '''
        pass

    def settings(self):
        '''
        Current method shows user interface settings window.
        '''
        self.sUi.show()

    def settings_export(self):
        data = self.timedb().copy_user('CATEGORY', '2')
        settingsSave = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', '/', 'CSV file (*.csv)')
        if settingsSave[0]:
            f = open(settingsSave[0], 'w+')
            with f:
                for d in data:
                    f.write(f'{d[2]}')

    # def table(self):
    #     lay = QtWidgets.QVBoxLayout()

    #     self.table = QtWidgets.QTableWidget()
    #     self.table.setColumnCount(5)
    #     self.table.setRowCount(2)
    #     self.table.resizeColumnsToContents()

    #     act_name = QtWidgets.QTableWidgetItem('Название события')
    #     self.table.setHorizontalHeaderItem(0, act_name)
    #     act_category = QtWidgets.QTableWidgetItem('Категория')
    #     self.table.setHorizontalHeaderItem(1, act_category)
    #     act_duration_time = QtWidgets.QTableWidgetItem('Длительность')
    #     self.table.setHorizontalHeaderItem(2, act_duration_time)
    #     act_user_date = QtWidgets.QTableWidgetItem('Дата создания')
    #     self.table.setHorizontalHeaderItem(3, act_user_date)
    #     act_comment = QtWidgets.QTableWidgetItem('Комментарий')
    #     self.table.setHorizontalHeaderItem(4, act_comment)

    #     name = QtWidgets.QTableWidgetItem(\
    #         self.timedb.get_custom_sql(f'SELECT activity_name FROM Activity \
    #             WHERE user_id = 43 and activity_id = {self.timedb.activity_id}'))
    #     self.table.setItem(0, 0, name)

    #     lay.addWidget(self.table)
    #     self.wUi.setLayout(lay)

    #     self.tabLe = QtWidgets.QTableWidget()
    #     self.tabLe.setColumnCount(6)
    #     self.tabLe.setRowCount(2)
    #     self.tabLe.resizeColumnsToContents()

    #     act_name = QtWidgets.QTableWidgetItem('Название события')
    #     self.tabLe.setHorizontalHeaderItem(0, act_name)
    #     act_category = QtWidgets.QTableWidgetItem('Категория')
    #     self.tabLe.setHorizontalHeaderItem(1, act_category)
    #     act_duration_time = QtWidgets.QTableWidgetItem('Длительность')
    #     self.tabLe.setHorizontalHeaderItem(2, act_duration_time)
    #     act_user_date = QtWidgets.QTableWidgetItem('Дата создания')
    #     self.tabLe.setHorizontalHeaderItem(3, act_user_date)
    #     act_comment = QtWidgets.QTableWidgetItem('Комментарий')
    #     self.tabLe.setHorizontalHeaderItem(4, act_comment)
    #     edit_del = QtWidgets.QTableWidgetItem('Изменить\Удалить')
    #     self.tabLe.setHorizontalHeaderItem(5, edit_del)

    #     name1 = QtWidgets.QTableWidgetItem(\
    #         self.timedb.get_custom_sql(f'SELECT activity_name FROM Activity \
    #             WHERE activity_id = 6'))
    #     self.tabLe.setItem(0, 0, name1)

    #     name2 = QtWidgets.QTableWidgetItem(\
    #         self.timedb.get_custom_sql(f'SELECT activity_name FROM Activity \
    #             WHERE activity_id = 7'))
    #     self.tabLe.setItem(1, 0, name2)

    #     lay.addWidget(self.tabLe)
    #     self.wUi.setLayout(lay)

    def view_table(self): # Table creation method.
        rows = 0
        self.lay = QtWidgets.QHBoxLayout()

        d1 = 'Бег'
        name1 = QtWidgets.QTableWidgetItem(d1)
        name1.setBackground(QtGui.QColor('Yellow'))

        rows += 1
        self.tUi.tableW.setRowCount(rows)
        self.tUi.tableW.setItem(0, 0, name1)

        self.lay.addWidget(self.tUi.tableW)
        self.wUi.setLayout(self.lay)

    def get_user_n_name(self):
        return self.user_n_name


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainUI()
    sys.exit(app.exec())
