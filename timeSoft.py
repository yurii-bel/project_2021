import sys
sys.path.append(".")

from PyQt5 import QtGui, QtWidgets, uic

# from logic.actions_ui import ActionsUI
from database.DBLogic.dblogic import DbLogic as db
from logic.time_add_activity import ActionsUI


class MainUI(QtWidgets.QMainWindow):
    '''
    This class implements Main Window of TimeSoft program.
    '''
    def __init__(self):
        super().__init__()
        self.timedb = db()

        # Нужно автоматизировать разделителей (module os).
        # Loading UI interfaces.
        self.mUi = uic.loadUi('design\\MainWindow.ui')  # Main window ui.
        # self.aUi = ActionsUI  # Loading ActionsUI class from logic.
        self.rUi = uic.loadUi('design\\register.ui')  # Registration window ui.
        self.lUi = uic.loadUi('design\\login.ui')  # Login window ui.
        self.sUi = uic.loadUi('design\\settings.ui')  # Settings window ui.
        self.tUi = uic.loadUi('design\\table.ui')
        self.wUi = self.mUi.viewWidget

        # Connecting buttons to slots.
        # All commented stuff is not yet realized.

        # Main UI 
        self.mUi.btn_plus.clicked.connect(self.add_action)

        self.mUi.btn_settings.clicked.connect(self.settings)
        self.mUi.btn_exit.clicked.connect(self.mUi.close)

        # Login UI
        self.lUi.login_btn_login.clicked.connect(self.login_check)
        self.lUi.login_btn_create_account.clicked.connect(self.registration)

        # Register UI
        self.rUi.register_btn_create.clicked.connect(self.login)
        self.rUi.register_btn_login.clicked.connect(self.registration_check)

        logo = QtGui.QPixmap('design\\img\\icons\\Logo.png')
        self.mUi.lbl_logoimg.setPixmap(logo)


        self.login()

    def add_action(self):
        '''
        Current method shows user interface action adding.
        '''
        self.aUi = ActionsUI()  # Loading ActionsUI class from logic.
        # self.table

    def settings(self):
        '''
        Current method shows user interface settings window.
        '''
        self.sUi.show()

    def login(self):
        '''
        Current method shows user interface login window.
        '''
        self.rUi.close()
        self.lUi.show()

    def login_check(self):
        login = self.lUi.login_lineedit_email.text()
        password = self.lUi.login_lineedit_password.text()

        self.info = self.timedb.login_user(login, password)

        # while self.info == 'error_name' or self.info == 'error_password':
        #     if self.info == 'error_name':
        #         QtWidgets.QMessageBox.question(self,'Ошибка!',\
        #         'Данный пользователь не найден. Зарегестрируйтесь.', QtWidgets.QMessageBox.Ok)
        #         self.login_check()
                
        #     elif self.info == 'error_password':
        #         QtWidgets.QMessageBox.question(self,'Ошибка!',\
        #         'Неверный пароль.', QtWidgets.QMessageBox.Ok)
        #         self.login_check()
            
        #     elif self.info == True:
        #         self.lUi.close()
        #         self.mUi.show()

            # QtWidgets.QMessageBox.question(self,'Ошибка!',\
            #     'Данный пользователь не найден. Зарегестрируйтесь.', QtWidgets.QMessageBox.Ok)
            # continue
                
        # while self.info == False:
            # QtWidgets.QMessageBox.question(self,'Ошибка!',\
            #     'Неверный пароль.', QtWidgets.QMessageBox.Ok)
        #     break
            

    def registration(self):
        '''
        Current method shows user interface registration window.
        '''
        self.lUi.close()
        self.rUi.show()

    def registration_check(self):
        login = self.rUi.register_lineEdit_name.text()
        email = self.rUi.register_lineEdit_email.text()
        password = self.rUi.register_lineEdit_password.text()

        self.timedb.register_user(login, email, password)
        self.rUi.close()
        self.lUi.show()

    def visualize(self, object):
        '''
        Current method displays table/graph/chart view containing all actions. 
        '''
        pass

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

    def view_table(self):
        rows = 0
        self.lay = QtWidgets.QHBoxLayout()
        
        d1 = self.timedb.get_custom_sql(f'SELECT activity_name FROM Activity')
        name1 = QtWidgets.QTableWidgetItem(d1[2:-3])
        name1.setBackground(QtGui.QColor('Yellow'))
        
        rows += 1
        self.tUi.tableW.setRowCount(rows)
        self.tUi.tableW.setItem(0, 0, name1)

        self.lay.addWidget(self.tUi.tableW)
        self.wUi.setLayout(self.lay)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainUI()
    sys.exit(app.exec())
