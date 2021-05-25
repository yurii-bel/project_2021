import sys
sys.path.append(".")

from PyQt5 import QtCore, QtGui, QtWidgets, uic

from logic.actions_ui import ActionsUI
from logic.dblogic import DbLogic as db


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    '''
    This class implements center positioning for icons in TableView widget
    '''
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.decorationSize = option.rect.size()


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
        self.aUi = ActionsUI # Loading ActionsUI class from logic.
        self.rUi = uic.loadUi('design\\register_d.ui') # Registration window ui.
        self.lUi = uic.loadUi('design\\login_d.ui') # Login window ui.
        self.sUi = uic.loadUi('design\\settings_d.ui') # Settings window ui.
        self.tUi = uic.loadUi('design\\table.ui') # Table ui.
        self.wUi = self.mUi.mainwindow_widget_view # Widget for viewing various data.

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

        # Connect TableView with mouseClick.
        self.tUi.tableW.clicked.connect(self.get_current_row_tableview)

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

        if self.db.user_input_check == '7':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Строка логина пуста. Пожалуйста, введите Ваш логин.',\
                    QtWidgets.QMessageBox.Ok)
        elif self.db.user_input_check == '8':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
            'Строка с паролем пуста. Пожалуйста, введите Ваш пароль.',\
                QtWidgets.QMessageBox.Ok)
        elif self.db.correct_login_info == False:
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
            'Неверный логин или пароль! ', QtWidgets.QMessageBox.Ok)

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

        if self.db.user_input_check == '1':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Данный пользователь уже зарегистрирован.', QtWidgets.QMessageBox.Ok)
        elif self.db.user_input_check == '2':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Данный email уже зарегистрирован.', QtWidgets.QMessageBox.Ok)
        elif self.db.user_input_check == '3':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Нельзя создать пустой логин пользователя.', QtWidgets.QMessageBox.Ok)
        elif self.db.user_input_check == '4':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Нельзя создать пустой email пользователя.', QtWidgets.QMessageBox.Ok)
        elif self.db.user_input_check == '5':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Нельзя создать пустой пароль пользователя.', QtWidgets.QMessageBox.Ok)
        elif self.db.user_input_check == '6':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Длина пароля должна быть не менее 8 символов.', QtWidgets.QMessageBox.Ok)
        else:
            self.rUi.close()
            self.lUi.show()

    def fill_tableview(self):
        pass

    def get_current_row_tableview(self, item):
        '''
        Current method displays clicked column and row of a choosen cell 
        in a TableView widget.
        '''
        print("You clicked on {0}x{1}".format(item.column(), item.row()))

    def add_action(self):
        '''
        Current method shows user interface action adding.
        '''
        self.act = self.aUi(self.user_n_name)  # Loading ActionsUI class from logic.
        self.act.show_add_event()

    def edit_action(self):
        self.act.show_edit_event()

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

    def view_table(self): # Table creation method.


        rows = self.db.table_rows_num
        self.lay = QtWidgets.QHBoxLayout()

        # d1 = 'Бег'
        # name1 = QtWidgets.QTableWidgetItem(d1)
        # name1.setBackground(QtGui.QColor('Yellow'))

        # rows += 1
        


        self.tUi.tableW.setRowCount(rows)
        for i in range(rows):
            # setting all activities data.
            self.tUi.tableW.setItem(i, 0, QtWidgets.QTableWidgetItem(self.db.activity_creation_date[i]))
            self.tUi.tableW.setItem(i, 1, QtWidgets.QTableWidgetItem(self.db.activity_category[i]))
            self.tUi.tableW.setItem(i, 2, QtWidgets.QTableWidgetItem(self.db.activity_name[i]))
            self.tUi.tableW.setItem(i, 3, QtWidgets.QTableWidgetItem(self.db.activity_duration[i]))
            self.tUi.tableW.setItem(i, 4, QtWidgets.QTableWidgetItem(self.db.activity_comment[i]))
            
            # # setting edit and delete icons to fields.
            # icon_edit = 'design\\img\\icons\\tableview_edit_icon.png'
            # icon_delete = 'design\\img\\icons\\tableview_delete_icon.png'

            # status_item_edit = QtWidgets.QTableWidgetItem()

            # status_icon_edit = QtGui.QIcon()
            # status_icon_edit.addPixmap(QtGui.QPixmap(icon_edit), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            # status_item_edit.setIcon(status_icon_edit)
            # self.tUi.tableW.setItem(i, 5, status_item_edit)

            # status_item_delete = QtWidgets.QTableWidgetItem()

            # status_icon_delete = QtGui.QIcon()
            # status_icon_delete.addPixmap(QtGui.QPixmap(icon_delete), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            # status_item_delete.setIcon(status_icon_delete)
            # self.tUi.tableW.setItem(i, 6, status_item_delete)

            # # coloring background cells for edit and delete.
            # self.tUi.tableW.item(i, 5).setBackground(QtGui.QColor(115, 103, 240))
            # self.tUi.tableW.item(i, 6).setBackground(QtGui.QColor(115, 103, 240))

            # # centering icons.
            # delegate = AlignDelegate(self.tUi.tableW)
            # self.tUi.tableW.setItemDelegate(delegate)


            # forbiding cell selection.
            self.tUi.tableW.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)


        self.lay.addWidget(self.tUi.tableW)
        self.wUi.setLayout(self.lay)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainUI()
    sys.exit(app.exec())
