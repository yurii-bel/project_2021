import sys
sys.path.append(".")

from PyQt5 import QtCore, QtGui, QtWidgets, uic

import psycopg2 as db
from psycopg2 import Error
from uuid import uuid4
import psycopg2.extras

import datetime
import re
import sys
sys.path.append('.')

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate


# ----------------------------------------------------------START-----timeSoft
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
        self.timedb = DbLogic

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

    # AUTHORIZATION BLOCK.
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

    # REGISTRATION BLOCK.
    def show_registration(self):
        '''
        Current method shows user interface registration window.
        '''
        self.lUi.close()
        self.rUi.show()

    def registration(self):
        login = self.rUi.register_lineEdit_name.text()
        email = self.rUi.register_lineEdit_email.text()
        password = self.rUi.register_lineEdit_password.text()

        self.timedb().register_user(login, email, password)

        if self.timedb().user_input_check == '1':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Данный пользователь уже зарегистрирован.', QtWidgets.QMessageBox.Ok)
        elif self.timedb().user_input_check == '2':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Данный email уже зарегистрирован.', QtWidgets.QMessageBox.Ok)
        elif self.timedb().user_input_check == '3':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Нельзя создать пустой логин пользователя.', QtWidgets.QMessageBox.Ok)
        elif self.timedb().user_input_check == '4':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Нельзя создать пустой email пользователя.', QtWidgets.QMessageBox.Ok)
        elif self.timedb().user_input_check == '5':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Нельзя создать пустой пароль пользователя.', QtWidgets.QMessageBox.Ok)
        elif self.timedb().user_input_check == '6':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Длина пароля должна быть не менее 8 символов.', QtWidgets.QMessageBox.Ok)
        else:
            self.rUi.close()
            self.lUi.show()

    def get_current_row_tableview(self, item): 
        '''
        Current method displays clicked column and row of a choosen cell 
        in a TableView widget.
        '''
        # #selected cell value.
        self.act_date = str(item.sibling(item.row(), 0).data())
        self.cat_name = str(item.sibling(item.row(), 1).data())
        self.actl_name = str(item.sibling(item.row(), 2).data())
        self.act_time = str(item.sibling(item.row(), 3).data())
        self.act_comment = str(item.sibling(item.row(), 1).data())

    def add_action(self):
        '''
        Current method shows user interface action adding.
        '''
        self.act = self.aUi(self.user_n_name)  # Loading ActionsUI class from logic.
        
        self.act.show_add_event()
        # self.act.add_event()
        
        # self.db.load_user_activities()
        # self.view_table()
        # print(self.db.activity_name)
        # print(self.act.add_event_status)


    def edit_action(self):
        self.act.show_edit_event(self.actl_name, self.act_time, self.act_date, self.cat_name, self.act_comment)
        self.tableview_updating()

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

# Table creation method.
    def view_table(self): 
        rows = self.db.table_rows_num
        self.lay = QtWidgets.QHBoxLayout()

        self.tUi.tableW.setRowCount(rows)
        
        for i in range(rows):
            # setting all activities data.
            self.tUi.tableW.setItem(i, 0, 
            QtWidgets.QTableWidgetItem(self.db.activity_creation_date[i]))
            self.tUi.tableW.setItem(i, 1, 
            QtWidgets.QTableWidgetItem(self.db.activity_category[i]))
            self.tUi.tableW.setItem(i, 2, 
            QtWidgets.QTableWidgetItem(self.db.activity_name[i]))
            self.tUi.tableW.setItem(i, 3, 
            QtWidgets.QTableWidgetItem(self.db.activity_duration[i]))
            self.tUi.tableW.setItem(i, 4, 
            QtWidgets.QTableWidgetItem(self.db.activity_comment[i]))
            
            # forbiding cell selection.
            self.tUi.tableW.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self.lay.addWidget(self.tUi.tableW)
        self.wUi.setLayout(self.lay)

# ----------------------------------------------------------END-----timeSoft.py

# ----------------------------------------------------------START----dblogic.py
class DbLogic:

    database = 'dt1vdgsvah47r'
    user = 'ryxcgrjdgvrsxx'
    password = '2e4d8cbc5b0f94259507584c6868f20ae0d4da79fdc618f6c2602d18045b2b61'
    host = 'ec2-54-74-60-70.eu-west-1.compute.amazonaws.com'

    def __init__(self):
        self.connection = db.connect(database=self.database, user=self.user, \
        password=self.password, host=self.host)

        self.cursor = self.connection.cursor()
        self.cursor2 = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        self.correct_login_info = False
        self.user_input_check = None

        self.activity_creation_date = []
        self.activity_category = []
        self.activity_name = []
        self.activity_duration = []
        self.activity_comment = []
        self.table_rows_num = 0 

        self.current_user_id = None

        self.current_user_n_id = None
        self.current_user_n_name = None
        self.current_user_n_telegram = None

        self.current_user_p_id = None
        self.current_user_p_email = None
        self.current_user_p_password = None

    def register_user(self, user_n_name, user_p_email, user_p_password):
        try:
            user_n_id = str(uuid4())
            user_p_id = str(uuid4())
            self.connection.autocommit = True

            self.cursor.execute(
                f'SELECT "USER_NAME".user_n_name = \'{user_n_name}\' FROM "USER_NAME"')
            # Сделано в Китае. Разработано в России.
            lst = str(self.cursor.fetchall())
            if 'True' in lst:
                self.user_input_check = '1'
                return 
            elif 'True' in lst:
                self.user_input_check = '2'
                return
            elif user_n_name == '':
                self.user_input_check = '3'
                return
            elif user_p_email == '':
                self.user_input_check = '4'
                return
            elif user_p_password == '':
                self.user_input_check = '5'
                return
            elif len(user_p_password) <= 7:
                self.user_input_check = '6'
                return

            self.cursor.execute('INSERT INTO "USER" (user_n_id, user_p_id)\
                VALUES (%s,%s) ON CONFLICT DO NOTHING', (user_n_id, user_p_id))

            self.cursor.execute('INSERT INTO "USER_NAME" (user_n_id, user_n_name)\
                VALUES (%s,%s) ON CONFLICT DO NOTHING', (user_n_id, user_n_name))

            self.cursor.execute('INSERT INTO "USER_PRIVATE" (user_p_id, user_p_email, user_p_password)\
                VALUES (%s,%s,%s) ON CONFLICT DO NOTHING', (user_p_id, user_p_email, user_p_password))

        except Exception:
            pass

    def login_user(self, user_n_name, user_p_password):
        try:
            self.connection.autocommit = True

            self.current_user_id = None

            self.current_user_n_id = None
            self.current_user_n_name = None
            self.current_user_n_telegram = None

            self.current_user_p_id = None
            self.current_user_p_email = None
            self.current_user_p_password = None

            if user_n_name == '':
                self.user_input_check = '7'
                return
            elif user_p_password == '':
                self.user_input_check = '8'
                return

            # working with USER_NAME table
            self.cursor.execute(
                f'SELECT user_n_id, user_n_name, user_n_telegram from "USER_NAME"')
            user_name_table_rows = self.cursor.fetchall()

            for row in user_name_table_rows:
                if user_n_name == row[1]:
                    self.current_user_n_id = row[0]
                    self.current_user_n_name = row[1]
                    self.current_user_n_telegram = row[2]
                    break
                else:
                    pass

            # working with USER table
            self.cursor.execute(
                f'SELECT user_id, user_n_id, user_p_id from "USER"')
            user_table_rows = self.cursor.fetchall()

            for row in user_table_rows:
                if self.current_user_n_id == row[1]:
                    self.current_user_id = row[0]
                    self.current_user_p_id = row[2]
                else:
                    pass

            # working with USER_PRIVATE table
            self.cursor.execute(
                f'SELECT user_p_id, user_p_email, user_p_password from "USER_PRIVATE"')
            user_private_table_rows = self.cursor.fetchall()

            for row in user_private_table_rows:
                if user_p_password == row[2] and self.current_user_p_id == row[0]:
                    self.current_user_p_email = row[1]
                    self.current_user_p_password = row[2]
                    self.correct_login_info = True
                    break
                else:
                    self.correct_login_info = False

            if self.correct_login_info == True: 
                self.load_user_activities()   # loading activities from db

        except Exception:
            pass
    
    def load_user_activities(self):

        # working with ACTIVITY table.
        self.activity_creation_date = []
        self.activity_category = []
        self.activity_name = []
        self.activity_duration = []
        self.activity_comment = []
        self.table_rows_num = 0  # The number of rows in current TableView widget.

        self.connection.autocommit = True
        self.cursor.execute(
            f'SELECT act_id, user_id, actl_name, act_time, act_date, cat_name,\
                act_comment from "ACTIVITY"')
        user_activities_table_rows = self.cursor.fetchall()
        # print(f':::: {user_activities_table_rows}')
        print(self.current_user_id)
        for row in user_activities_table_rows:
            if row[1] == self.current_user_id:
                # print(f'row[1]: {row[1]} | self.current_user_id: {self.current_user_id:}')
                # print(f'act id: {row[0]}| id: {row[1]}| activity: {row[2]}' )
                self.activity_creation_date.append(str(row[4]))  # act_date
                self.activity_category.append(str(row[5]))  # cat_name
                self.activity_name.append(str(row[2]))  # actl_name
                self.activity_duration.append(str(row[3]))  # act_time
                self.activity_comment.append(str(row[6]))  # act_comment

        self.table_rows_num = len(self.activity_name)      
                # print(f'{row[4]}')
        # print(f'\nDate: {self.activity_creation_date} \nCategory: \
        #     {self.activity_category} \nActivity: {self.activity_name} \
        #         \nDuration: {self.activity_duration} \nComment: {self.activity_comment}')
        

    def drop_user(self, user_n_name):
        try:
            self.connection.autocommit = True
            
            user_id = self.get_user_n_id(user_n_name)

            self.cursor.execute(\
                'DELETE FROM "USER" WHERE user_n_id = %(userID)s',\
                                {'userID': user_id})
        except Exception:
            pass

    def get_user_n_id(self, user):
        try:
            self.cursor2.execute(
                'SELECT user_n_id FROM "USER_NAME"\
                    WHERE user_n_name = %(user)s', {'user': user})
            return str(self.cursor2.fetchone())[2:-2]
        except Exception:
            pass

    def get_user_id(self, user_n_id):
        try:
            self.cursor2.execute(\
                'SELECT user_id FROM "USER"\
                    WHERE user_n_id = %(user_n_id)s', {'user_n_id': user_n_id})
            return str(self.cursor2.fetchall())[2:-2]
        except Exception:
            pass

    def get_actl_id(self, user, actl_name, cat_name):
        self.connection.autocommit = True
        user_n_id = self.get_user_n_id(user)
        user_id = self.get_user_id(user_n_id)

        self.cursor2.execute(\
            f'SELECT actl_id FROM "ACTIVITY_LIST" WHERE\
                (user_id, actl_name, cat_name) = (\'{user_id}\', \'{actl_name}\', \'{cat_name}\')')
        for row in self.cursor2.fetchall():
            return row[0]

    def get_act_id(self, user, actl_name, act_time, act_date, cat_name, act_comment):
        self.connection.autocommit = True
        user_n_id = self.get_user_n_id(user)
        user_id = self.get_user_id(user_n_id)

        self.cursor2.execute(\
            f'SELECT act_id FROM "ACTIVITY" WHERE\
                (user_id, actl_name, act_time, act_date, cat_name, act_comment) =\
                    (\'{user_id}\', \'{actl_name}\', \'{act_time}\', \'{act_date}\',\
                        \'{cat_name}\', \'{act_comment}\')')
        for row in self.cursor2.fetchall():
            return row[0]

    def get_user_categories(self, user):
        try:
            self.connection.autocommit = True
            user_n_id = self.get_user_n_id(user)
            user_id = self.get_user_id(user_n_id)
            self.cursor2.execute(\
                'SELECT cat_name FROM "CATEGORY"\
                    WHERE user_id = %(userID)s', {'userID': user_id})
            categs = []
            for row in self.cursor2.fetchall():
                categs += row
            return categs
        except Exception:
            pass

    def copy_user(self, table_name, column):
        try:
            with self.connection:
                with self.cursor:
                    self.cursor.execute(f'SELECT * FROM "{table_name}"\
                        WHERE USER_ID = \'{column}\'')
                    return self.cursor.fetchall()
        except (Exception, Error) as error:
            return f'{error}'

    def add_event(self, user, actl_name, act_time, act_date, cat_name,\
        act_comment):

        self.connection.autocommit = True
        user_n_id = self.get_user_n_id(user)
        user_id = self.get_user_id(user_n_id)

        self.cursor2.execute(\
            f'SELECT cat_name FROM "CATEGORY" WHERE user_id = \'{user_id}\'')
        user_categories = self.cursor2.fetchall()
        for row in user_categories:
            if cat_name == row[0]:
                break
        else:
            self.cursor2.execute(\
                f'INSERT INTO "CATEGORY" (user_id, cat_name) VALUES (%s,%s)',\
                    (user_id, cat_name))

        self.cursor2.execute(\
            f'INSERT INTO "ACTIVITY_LIST" (user_id, actl_name, cat_name)\
                VALUES (%s,%s,%s) ON CONFLICT DO NOTHING', (user_id, actl_name, cat_name))

        self.cursor2.execute('INSERT INTO "ACTIVITY" (user_id, actl_name,\
                    act_time, act_date, cat_name, act_comment)\
                        VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING' ,\
                    (user_id, actl_name, act_time, act_date, cat_name, act_comment))

    def edit_event(self, user, actl_name, act_time, act_date, cat_name,\
        act_comment, act_id, actl_id):

        self.connection.autocommit = True
        user_n_id = self.get_user_n_id(user)
        user_id = self.get_user_id(user_n_id)

        self.cursor2.execute(\
            f'SELECT cat_name FROM "CATEGORY" WHERE user_id = \'{user_id}\'')
        user_categories = self.cursor2.fetchall()
        for row in user_categories:
            if cat_name == row[0]:
                break
        else:
            self.cursor2.execute(\
                f'INSERT INTO "CATEGORY" (user_id, cat_name) VALUES (%s,%s)',\
                    (user_id, cat_name))

        self.cursor2.execute(\
            f'UPDATE "ACTIVITY_LIST" SET (actl_name, cat_name) = (\'{actl_name}\',\
                \'{cat_name}\') WHERE actl_id = \'{actl_id}\' ON CONFLICT DO NOTHING')
        
        self.cursor2.execute(\
            f'UPDATE "ACTIVITY" SET (actl_name, act_time, act_date, cat_name, \
                act_comment) = (\'{actl_name}\', \'{act_time}\', \'{act_date}\',\
                    \'{cat_name}\', \'{act_comment}\') WHERE act_id = \'{act_id}\'\
                     ON CONFLICT DO NOTHING')

    def drop_event(self, user, actl_name):
        try:
            self.connection.autocommit = True
            user_n_id = self.get_user_n_id(user)
            user_id = self.get_user_id(user_n_id)

            self.cursor2.execute(\
                f'DELETE FROM "ACTIVITY"\
                    WHERE user_id = \'{user_id}\' and actl_name = \'{actl_name}\'')

            self.cursor2.execute(\
                f'DELETE FROM "ACTIVITY_LIST"\
                    WHERE user_id = \'{user_id}\' and actl_name = \'{actl_name}\'')
        except Exception:
            pass

    def drop_category(self, user, cat_name):
        try:
            self.connection.autocommit = True
            user_n_id = self.get_user_n_id(user)
            user_id = self.get_user_id(user_n_id)

            self.cursor2.execute(\
                f'DELETE FROM "CATEGORY"\
                    WHERE user_id = \'{user_id}\' and cat_name = \'{cat_name}\'')
        except Exception:
            pass

# ----------------------------------------------------------END----dblogic.py



# ----------------------------------------------------------START----actions_ui.py

class ActionsUI(QtWidgets.QMainWindow):
    '''
    This class implements adding and editing actions.
    '''
    def __init__(self, user):
        super().__init__()
        # Creating database instance.
        self.timedb = DbLogic

        # Getting current user name.
        self.user_n_name = user

        # Loading appropriate UI's.
        self.aUi = uic.loadUi('design\\add_event_d.ui')
        self.eUi = uic.loadUi('design\\edit_event_d.ui')

        # Connecting buttons to appropriate slots.
        self.aUi.add_event_btn_add.clicked.connect(self.add_event)
        self.aUi.add_event_btn_cancel.clicked.connect(self.aUi.close)
        self.aUi.add_event_btn_exit.clicked.connect(self.aUi.close)

        self.eUi.edit_event_btn_save.clicked.connect(self.edit_event)
        # self.eUi.edit_event_btn_del.clicked.connect(self.delete_event)
        self.eUi.edit_event_btn_exit.clicked.connect(self.eUi.close)

        # Connecting line edits to appropriate slots.
        self.aUi.add_event_lineEdit_name.textChanged.connect(
            self.suppose_category)
        
        # Get MainUi class from timeSoft (linked).
        # self.timeSoft = MainUI

        # Extra variables.
        self.add_event_status = None
        self.edit_event_status = None
        self.user_input_check = None

    def ui_add_event_preparations(self):
        # Settings for 'a_dE_date' control element.
        self.aUi.add_event_dateEdit.setCalendarPopup(True)
        self.aUi.add_event_dateEdit.setDate(QDate(QDate.currentDate()))
        self.aUi.add_event_dateEdit.setMaximumDate(QDate(QDate.currentDate()))
        
        categs, i = self.timedb().get_user_categories(self.user_n_name), 0
        for categ in categs:
            self.aUi.add_event_comboBox_category.insertItem(i, categ)
            i += 1

    def ui_edit_event_preparations(self, settings):
        self.eUi.edit_event_dateEdit.setCalendarPopup(True)
        self.eUi.edit_event_dateEdit.setMaximumDate(QDate(QDate.currentDate()))

        categs, i = self.timedb().get_user_categories(self.user_n_name), 0
        for categ in categs:
            self.eUi.edit_event_comboBox_category.insertItem(i, categ)
            i += 1

        date_ = datetime.datetime.strptime(settings[2], '%Y-%m-%d')
        for d in [date_.timetuple()]:
            year = int(d[0])
            month = int(d[1])
            day = int(d[2])
            date = QDate(year, month, day)
        
        self.eUi.edit_event_lineEdit_name.setText(settings[0])
        self.eUi.edit_event_comboBox_category.setCurrentText(settings[3])
        self.eUi.edit_event_lineEdit_time.setText(settings[1])
        self.eUi.edit_event_dateEdit.setDate(date)
        self.eUi.edit_event_plaintextedit_comment.setPlainText(settings[4])

    def show_add_event(self):
        self.ui_add_event_preparations()
        self.aUi.show()

    def show_edit_event(self, actl_name=str, act_time=str, act_date=None,\
         cat_name=str, act_comment=None):
        settings = [actl_name, act_time, act_date, cat_name, act_comment]
        self.ui_edit_event_preparations(settings)

        self.act_id = self.timedb().get_act_id(self.user_n_name, actl_name,\
             act_time, act_date, cat_name, act_comment)

        self.actl_id = self.timedb().get_actl_id(self.user_n_name, actl_name, cat_name)

        self.eUi.show()

    def add_event(self):
        # Getting all info, entered by user.
        title = self.aUi.add_event_lineEdit_name.text()        
        category = self.aUi.add_event_comboBox_category.currentText()
        duration = self.aUi.add_event_lineEdit_time.text()
        date = self.aUi.add_event_dateEdit.date()
        comment = self.aUi.add_event_plaintextedit_comment.toPlainText()

        if title == '':
            self.user_input_check = '1'
            return
        elif category == '':
            self.user_input_check = '2'
            return
        elif duration == '':
            self.user_input_check = '3'
            return

        date_ = datetime.date(date.year(), date.month(), date.day())
        str_date = date_.strftime('%Y-%m-%d')
        
        int_duration = int(''.join(filter(str.isdigit, duration)))

        # Writing all changes to db and closing 'Add Event' win.
        self.timedb().add_event(self.user_n_name, title, int_duration,\
            str_date, category, comment)  
        
        self.aUi.close()
        self.add_event_status = True 

        self.timedb().load_user_activities()
        # self.timeSoft.view_table()
        # print(self.timedb().activity_name)

    def suppose_category(self):
        pass

    def edit_event(self):
        title = self.eUi.edit_event_lineEdit_name.text()        
        category = self.eUi.edit_event_comboBox_category.currentText()
        duration = self.eUi.edit_event_lineEdit_time.text()
        date = self.eUi.edit_event_dateEdit.date()
        comment = self.eUi.edit_event_plaintextedit_comment.toPlainText()

        date_ = datetime.date(date.year(), date.month(), date.day())
        str_date = date_.strftime('%Y-%m-%d')
        
        int_duration = int(''.join(filter(str.isdigit, duration)))

        # Writing all changes to db and closing 'Add Event' win.
        self.timedb().edit_event(self.user_n_name, title, int_duration,\
            str_date, category, comment, self.act_id, self.actl_id)
        self.eUi.close()
        self.edit_event_status = True

# ----------------------------------------------------------END----actions_ui.py

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainUI()
    sys.exit(app.exec())
