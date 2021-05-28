import sys
import os
import datetime
import csv

sys.path.append(".")

from PyQt5 import QtCore, QtGui, QtWidgets, uic

import psycopg2 as db
from psycopg2 import Error
from uuid import uuid4
import psycopg2.extras


# ----------------------------------------------------------START-----timeSoft
class AlignDelegate(QtWidgets.QStyledItemDelegate):
    '''
    This class implements center positioning for icons in TableView widget
    '''
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.decorationSize = option.rect.size()


class MainUI(QtWidgets.QMainWindow):
    # TODO:
    # Set placeholders everywhere.
    # Нужно автоматизировать разделителей (module os).
    # Connect all buttons to appropriate slots.
    def __init__(self):
        super().__init__()
        # Creating database instance.
        self.timedb = DbLogic()

        # Loading UI interfaces.
        self.mUi = uic.loadUi('design\\MainWindow_d.ui') # Main window ui.
        self.aUi = ActionsUI # Loading ActionsUI class from logic.
        self.rUi = uic.loadUi('design\\register_d.ui') # Registration window ui.
        self.lUi = uic.loadUi('design\\login_d.ui') # Login window ui.
        self.sUi = uic.loadUi('design\\settings_d.ui') # Settings window ui.
        self.tUi = uic.loadUi('design\\table.ui') # Table ui.
        self.wUi = self.mUi.mainwindow_widget_view # Widget for viewing various data.

        # Various settings for different UI elements, such as connecting 
        # buttons to slots, setting menubars and status bar.
        self.initUI()

        # Connect TableView with mouseClick.
        self.tUi.tableW.clicked.connect(self.get_current_row_tableview)

        # When starting a program, first login UI appears.
        self.show_login()

    def initUI(self):
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
        self.sUi.settings_btn_import.clicked.connect(self.settings_import)
        self.sUi.settings_btn_undo.clicked.connect(self.sUi.close)
        self.sUi.settings_btn_apply.clicked.connect(self.settings_save)        

    # AUTHORIZATION BLOCK.
    def show_login(self):
        '''
        Current method shows user interface login window.
        '''
        self.rUi.close()
        self.lUi.show()

    def login(self):
        login = self.lUi.login_lineedit_email.text()
        password = self.lUi.login_lineedit_password.text()

        self.timedb.login_user(login, password)

        if self.timedb.user_input_check == '7':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Строка логина пуста. Пожалуйста, введите Ваш логин.',\
                    QtWidgets.QMessageBox.Ok)
        elif self.timedb.user_input_check == '8':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
            'Строка с паролем пуста. Пожалуйста, введите Ваш пароль.',\
                QtWidgets.QMessageBox.Ok)
        elif self.timedb.correct_login_info == False:
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
            'Неверный логин или пароль! ', QtWidgets.QMessageBox.Ok)

        elif self.timedb.correct_login_info == True:
            self.user_n_name = login
            self.timedb.get_logged_user_data(user_login=self.user_n_name,\
                item='set_working_user')
            self.timedb.set_logged_user_data(user_login=self.user_n_name,\
                item='set_working_user')
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

        self.timedb.register_user(login, email, password)

        if self.timedb.user_input_check == '1':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Данный пользователь уже зарегистрирован.', QtWidgets.QMessageBox.Ok)
        elif self.timedb.user_input_check == '2':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Данный email уже зарегистрирован.', QtWidgets.QMessageBox.Ok)
        elif self.timedb.user_input_check == '3':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Нельзя создать пустой логин пользователя.', QtWidgets.QMessageBox.Ok)
        elif self.timedb.user_input_check == '4':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Нельзя создать пустой email пользователя.', QtWidgets.QMessageBox.Ok)
        elif self.timedb.user_input_check == '5':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Нельзя создать пустой пароль пользователя.', QtWidgets.QMessageBox.Ok)
        elif self.timedb.user_input_check == '6':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Длина пароля должна быть не менее 8 символов.', QtWidgets.QMessageBox.Ok)
        else:
            self.rUi.close()
            self.lUi.show()

    # FOR TABLE AND EDIT_EVENT.
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
        return self.actl_name

    # EDIT ACTION BLOCK. uses ActionsUI class, method add_event().
    def add_action(self):
        '''
        Current method shows user interface action adding.
        '''
        self.act = self.aUi(self.user_n_name)  # Loading ActionsUI class from logic.
        
        self.act.show_add_event()
        # self.lay.removeWidget(self.wUi)
        # self.view_table()

    # EDIT ACTION BLOCK. uses ActionsUI class, method show_edit_event().
    def edit_action(self):
        self.act.show_edit_event(self.actl_name, self.act_time, self.act_date,\
            self.cat_name, self.act_comment)
        self.tableview_updating()

    # SETTINGS BLOCK.
    def settings(self):
        # Shows settings win.
        self.sUi.show()

    def settings_export(self):
        data = self.timedb.get_logged_user_data(item='get_user_activities')
        try:
            settingsSave, ok = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file',\
                '/', 'CSV file (*.csv)')
            if settingsSave[0]:
                with open(settingsSave[0], 'w+', newline='') as f:
                    writer = csv.writer(f)
                    for d in data:
                        writer.writerow(d)

        except Exception:
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Экспорт не удался.', QtWidgets.QMessageBox.Ok)
        if ok:
            QtWidgets.QMessageBox.question(self, 'Успех!',\
                'Экспорт успешно завершён!', QtWidgets.QMessageBox.Ok)

    def settings_import(self):
        try:
            settingsLoad, ok = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file',\
                '/', 'CSV file (*.csv)')
            if settingsLoad[0]:
                with open(settingsLoad[0], 'r+') as f:
                    reader = csv.reader(f, delimiter=',')
                    for row in reader:
                        if not self.timedb.set_logged_user_data(item='check_event_data',\
                            add_params=row) == True:
                            self.timedb.set_logged_user_data(item='add_event', add_params=row)

        except Exception:
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Импорт не удался.', QtWidgets.QMessageBox.Ok)
        if ok:
            QtWidgets.QMessageBox.question(self, 'Успех!',\
                'Импорт успешно завершён!', QtWidgets.QMessageBox.Ok)
        

    def settings_save(self):
        self.timedb.get_logged_user_data(item='get_user_p_id')
        email = self.sUi.settings_lineedit_email.text()
        old_pass = self.sUi.settings_lineedit_oldpass.text()
        new_pass = self.sUi.settings_lineedit_newpass.text()
        repeat_new_pass = self.sUi.settings_lineedit_repnewpass.text()

        if not email == self.timedb.get_logged_user_data(item='get_user_email'):
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Введённый email не совпадает с зарегестрированным.',\
                    QtWidgets.QMessageBox.Ok)
        elif not old_pass == self.timedb.get_logged_user_data(item='get_user_password'):
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Текущий пароль неверный.',\
                    QtWidgets.QMessageBox.Ok)
        elif len(new_pass) <= 7:
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Пароль должен состоять миниммум из восьми символов.',\
                    QtWidgets.QMessageBox.Ok)
        elif not new_pass == repeat_new_pass:
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Проверьте правильность ввода новых паролей.',\
                    QtWidgets.QMessageBox.Ok)
        elif len(repeat_new_pass) <= 7:
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Пароль должен состоять миниммум из восьми символов.',\
                    QtWidgets.QMessageBox.Ok)
        else:
            self.timedb.set_logged_user_data(item='change_password',\
                edit_params=[repeat_new_pass, email])
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                    'Пароль успешно изменён.', QtWidgets.QMessageBox.Ok)
            self.sUi.close()


    # TABLE VIEWING BLOCK. uses DbLogic class.
    def view_table(self): 
        # Getting all user activities.
        rows = self.timedb.get_logged_user_data(item='get_user_activities')
        
        # Creating layout fro widget.
        lay = QtWidgets.QHBoxLayout()

        # Setting row count according to user activities quantity.
        self.tUi.tableW.setRowCount(len(rows))
        
        i = 0
        for row in rows:
            # If user have left some comment, 
            # in the name of activity * appears.
            if not row[4] == '' and not row[4] == None:
                row[0] = row[0] + '*'
        
            self.tUi.tableW.setItem(i, 0, 
            QtWidgets.QTableWidgetItem(row[3]))
            self.tUi.tableW.setItem(i, 1, 
            QtWidgets.QTableWidgetItem(row[0]))
            self.tUi.tableW.setItem(i, 2, 
            QtWidgets.QTableWidgetItem(row[1]))
            self.tUi.tableW.setItem(i, 3, 
            QtWidgets.QTableWidgetItem(row[2]))
            i += 1
        
        # Forbiding cell selection.
        self.tUi.tableW.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        # Resizing table columns to its contents.
        self.tUi.tableW.resizeColumnsToContents()

        lay.addWidget(self.tUi.tableW)
        self.wUi.setLayout(lay)

    def update_view_table(self):
        rows = self.timedb.get_logged_user_data(item='get_user_activities')

        self.tUi.tableW.setRowCount(rows)
        
        i = 0
        for row in rows:
            # If user have left some comment, 
            # in the name of activity * appears.
            if not row[4] == '':
                row[0] = row[0] + '*'

            self.tUi.tableW.setItem(i, 0, 
            QtWidgets.QTableWidgetItem(row[2]))
            self.tUi.tableW.setItem(i, 1, 
            QtWidgets.QTableWidgetItem(row[3]))
            self.tUi.tableW.setItem(i, 2, 
            QtWidgets.QTableWidgetItem(row[0]))
            self.tUi.tableW.setItem(i, 3, 
            QtWidgets.QTableWidgetItem(row[1]))
            i += 1
        
        # Forbiding cell selection.
        self.tUi.tableW.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        # Resizing table columns to its contents.
        self.tUi.tableW.resizeColumnsToContents()

        self.lay.addWidget(self.tUi.tableW)
        self.wUi.setLayout(self.lay)

# ----------------------------------------------------------END-----timeSoft.py

# -------------------------------------0--------------------START----dblogic.py
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

    # REGISTRATION AND AUTHORIZATION BLOCKS.
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

    def get_logged_user_data(self, user_login=None, item=None, params=None):
        # params[0] = actl_name
        # params[1] = act_time
        # params[2] = act_date
        # params[3] = cat_name
        # params[4] = act_comment
        
        # Setting working user in db.
        if item == 'set_working_user':
            self.cursor.execute(\
                f'SELECT user_n_id FROM "USER_NAME" WHERE user_n_name = \'{user_login}\'')
            user_n_id = str(self.cursor.fetchall())[2:-3]

            self.cursor.execute(\
                f'SELECT user_id FROM "USER" WHERE user_n_id = {user_n_id}')
            self.user_id = str(self.cursor.fetchall())[2:-3]
            return self.user_id
        
        # Getting actl_id.
        elif item == 'get_actl_id':
            self.cursor.execute(\
            f'SELECT actl_id FROM "ACTIVITY_LIST" WHERE\
                (user_id, actl_name, cat_name) = (\'{self.user_id}\', \'{params[1]}\', \'{params[0]}\')')
            return str(self.cursor.fetchall())[2:-3]
        
        # Getting act_id.
        elif item == 'get_act_id':
            self.cursor.execute(\
            f'SELECT act_id FROM "ACTIVITY" WHERE\
                (user_id, actl_name, act_time, act_date, cat_name, act_comment) =\
                    (\'{self.user_id}\', \'{params[1]}\', \'{params[2]}\', \'{params[3]}\',\
                        \'{params[0]}\', \'{params[4]}\')')
            return str(self.cursor.fetchall())[2:-3]

        # Getting user_p_id.
        elif item == 'get_user_p_id':
            self.cursor.execute(\
                f'SELECT user_p_id FROM "USER" WHERE user_id = \'{self.user_id}\'')
            self.user_p_id = str(self.cursor.fetchall())[3:-4]
            return self.user_p_id

        # Getting user email.
        elif item == 'get_user_email':
            self.cursor.execute(\
                f'SELECT user_p_email FROM "USER_PRIVATE" WHERE\
                    user_p_id = \'{self.user_p_id}\'')
            return str(self.cursor.fetchall())[3:-4]

        # Getting user password.
        elif item == 'get_user_password':
            self.cursor.execute(\
                f'SELECT user_p_password FROM "USER_PRIVATE" WHERE\
                    user_p_id = \'{self.user_p_id}\'')
            return str(self.cursor.fetchall())[3:-4]

        # For getting user categories.    
        elif item == 'get_user_categories':
            self.cursor2.execute(\
                f'SELECT cat_name FROM "CATEGORY" WHERE user_id = \'{self.user_id}\'')
            self.user_categories = []
            for row in self.cursor2.fetchall():
                self.user_categories += row
            return self.user_categories

        # For getting all user activities.
        elif item == 'get_user_activities':
            self.cursor2.execute(\
                f'SELECT cat_name, actl_name, act_time, act_date, act_comment\
                    FROM "ACTIVITY" WHERE user_id = \'{self.user_id}\'')
            user_activities = []
            for row in self.cursor2.fetchall():
                # Setting date in str fromat.
                date_ = row[3].strftime('%Y-%m-%d')
                row[3] = date_
                # Setting duration in str fromat.
                duration = str(row[2])
                row[2] = duration
                user_activities.append(row)
            return user_activities
    

    def set_logged_user_data(self, user_login=None, item=None, add_params=None, edit_params=None):
        # params[0] = cat_name
        # params[1] = actl_name
        # params[2] = act_time
        # params[3] = act_date
        # params[4] = act_comment

        # Setting working user in db.
        if item == 'set_working_user':
            self.user_id = self.get_logged_user_data(user_login=user_login, item='set_working_user')
            return self.user_id

        # Storing user_p_id
        self.user_p_id = self.get_logged_user_data(item='get_user_p_id')

        # Сhecking for an existing record in db.
        if item == 'check_event_data':
            # Storing actl_id, using get_logged_user_data(). 
            self.actl_id = self.get_logged_user_data(\
                item='get_actl_id', params=[add_params[0],add_params[1]])

            # Storing act_id, using get_logged_user_data().
            self.act_id = self.get_logged_user_data(\
                item='get_act_id', params=[add_params[0], add_params[1],\
                    add_params[2], add_params[3], add_params[4]])
                    
            # Checking for matching same category in db.
            self.user_categories = self.get_logged_user_data(item='get_user_categories')
            for row in self.user_categories:
                if row == add_params[0]:
                    break
            else: # If not matching, adding category to db.
                self.cursor2.execute(\
                    f'INSERT INTO "CATEGORY" (user_id, cat_name) VALUES (%s,%s)',\
                        (self.user_id, add_params[0]))
                
                self.connection.commit()

            # Checking for matching same data in ACTIVITY_LIST table.
            self.cursor.execute(\
                f'SELECT (actl_name, cat_name) FROM "ACTIVITY_LIST" WHERE user_id =\
                    \'{self.user_id}\'')

            check_activity_list = self.cursor.fetchall()
            for row in check_activity_list:
                if f'({add_params[1]},{add_params[0]})' == row[0]: # If data matches, stop func.
                    return True
            
            # Checking for matching same data in ACTIVITY table.
            self.cursor.execute(\
                f'SELECT (cat_name, actl_name, act_time, act_date, act_comment)\
                    FROM "ACTIVITY" WHERE user_id = \'{self.user_id}\'')

            check_activity = self.cursor.fetchall()
            for row in check_activity:
                if f'({add_params[0]},{add_params[1]},{add_params[2]},{add_params[3]},{add_params[4]})'\
                    == row[0]:  # If data matches, stop func.
                    return True

        # Adding event as itself.
        elif item == 'add_event':
            self.cursor2.execute(\
                f'INSERT INTO "ACTIVITY_LIST" (user_id, actl_name, cat_name)\
                    VALUES (%s,%s,%s) ON CONFLICT DO NOTHING', (self.user_id,\
                        add_params[1], add_params[0]))

            self.cursor2.execute('INSERT INTO "ACTIVITY" (user_id, actl_name,\
                        act_time, act_date, cat_name, act_comment)\
                            VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING' ,\
                        (self.user_id, add_params[1], add_params[2], add_params[3], add_params[0],\
                            add_params[4]))
            
            self.connection.commit()
                            
        # Editing existing event in db.
        elif item == 'edit_event':
            self.cursor2.execute(\
                f'UPDATE "ACTIVITY_LIST" SET (actl_name, cat_name) = (\'{edit_params[1]}\',\
                    \'{edit_params[0]}\') WHERE actl_id = \'{self.actl_id}\'')
            
            self.cursor2.execute(\
                f'UPDATE "ACTIVITY" SET (actl_name, act_time, act_date, cat_name, \
                    act_comment) = (\'{edit_params[1]}\', \'{edit_params[2]}\', \'{edit_params[3]}\',\
                        \'{edit_params[0]}\', \'{edit_params[4]}\') WHERE act_id = \'{self.act_id}\'')
    
            self.connection.commit()

        # Deleting existing event.
        elif item == 'del_event':
            self.cursor.execute(\
                f'DELETE FROM "ACTIVITY_LIST" WHERE user_id = \'{self.user_id}\' and \
                    actl_name = \'{add_params[1]}\' and cat_name = \'{add_params[0]}\'')

            self.cursor.execute(\
                f'DELETE FROM "ACTIVITY" WHERE user_id = \'{self.user_id}\' and \
                    actl_name = \'{add_params[1]}\' and act_time = \'{add_params[2]}\' \
                        and act_date = \'{add_params[3]}\' and cat_name = \
                            \'{add_params[0]}\' and act_comment = \'{add_params[4]}\'')
            
            self.connection.commit()

        # Changing old user password to new.
        elif item == 'change_password':
            self.cursor2.execute(\
                f'UPDATE "USER_PRIVATE" SET user_p_password = \'{edit_params[0]}\'\
                    WHERE user_p_id = \'{self.user_p_id}\' and user_p_email =\
                        \'{edit_params[1]}\'')
            
            self.connection.commit()

    def update_user_activities(self, user):
        self.connection.autocommit = True
        user_n_id = self.get_user_n_id(user)
        user_id = self.get_user_id(user_n_id)

        self.cursor.execute(
            f'SELECT act_id, actl_name, act_time, act_date, cat_name,\
                act_comment from "ACTIVITY" WHERE user_id = \'{user_id}\'')
        user_activities_table_rows = self.cursor.fetchall()
        for row in user_activities_table_rows:
            # print(f'row[1]: {row[1]} | self.current_user_id: {self.current_user_id:}')
            # print(f'act id: {row[0]}| id: {row[1]}| activity: {row[2]}' )
            self.activity_creation_date.append(str(row[3]))  # act_date
            self.activity_category.append(str(row[4]))  # cat_name
            self.activity_name.append(str(row[1]))  # actl_name
            self.activity_duration.append(str(row[2]))  # act_time
            self.activity_comment.append(str(row[5]))  # act_comment

        self.table_rows_num = len(self.activity_name)      
        

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
    

    def copy_user(self, table_name, column):
        try:
            with self.connection:
                with self.cursor:
                    self.cursor.execute(f'SELECT * FROM "{table_name}"\
                        WHERE USER_ID = \'{column}\'')
                    return self.cursor.fetchall()
        except (Exception, Error) as error:
            return f'{error}'

# ----------------------------------------------------------END----dblogic.py



# ----------------------------------------------------------START----actions_ui.py

class ActionsUI(QtWidgets.QMainWindow):
    '''
    This class implements adding and editing actions.
    '''
    def __init__(self, user):
        super().__init__()
        # Creating database instance.
        self.timedb = DbLogic()

        # Setting working user in db.
        self.timedb.get_logged_user_data(user_login=user, item='set_working_user')
        self.timedb.set_logged_user_data(user_login=user, item='set_working_user')

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

        # Extra variables.
        self.add_event_status = None
        self.edit_event_status = None
        self.user_input_check = None

    # Preparations for add_event_ui showing.
    def init_add_event_ui(self):
        # Setting calendar popup and current date in date field. Also, forbidding 
        # selecting the next day in date field.
        self.aUi.add_event_dateEdit.setCalendarPopup(True)
        self.aUi.add_event_dateEdit.setDate(QtCore.QDate(QtCore.QDate.currentDate()))
        self.aUi.add_event_dateEdit.setMaximumDate(QtCore.QDate(QtCore.QDate.currentDate()))
        
        # Updating user categories for combobox element.
        categs, i = self.timedb.get_logged_user_data(item='get_user_categories'), 0
        for categ in categs:
            self.aUi.add_event_comboBox_category.insertItem(i, categ)
            i += 1

    # Preparations for edit_event_ui showing.
    def init_edit_event_ui(self, settings):
        self.eUi.edit_event_dateEdit.setCalendarPopup(True)
        self.eUi.edit_event_dateEdit.setMaximumDate(QtCore.QDate(QtCore.QDate.currentDate()))

        categs, i = self.timedb.get_logged_user_data(item='get_user_categories'), 0
        for categ in categs:
            self.eUi.edit_event_comboBox_category.insertItem(i, categ)
            i += 1

        date_ = datetime.datetime.strptime(settings[2], '%Y-%m-%d')
        for d in [date_.timetuple()]:
            year = int(d[0])
            month = int(d[1])
            day = int(d[2])
            date = QtCore.QDate(year, month, day)
        
        self.eUi.edit_event_lineEdit_name.setText(settings[0])
        self.eUi.edit_event_comboBox_category.setCurrentText(settings[3])
        self.eUi.edit_event_lineEdit_time.setText(settings[1])
        self.eUi.edit_event_dateEdit.setDate(date)
        self.eUi.edit_event_plaintextedit_comment.setPlainText(settings[4])

    def show_add_event(self):
        self.init_add_event_ui()
        self.aUi.show()

    def show_edit_event(self, actl_name=str, act_time=str, act_date=None,\
         cat_name=str, act_comment=None):
        
        settings = [actl_name, act_time, act_date, cat_name, act_comment]
        self.init_edit_event_ui(settings)

        self.act_id = self.timedb.get_logged_user_data(item='get_act_id',\
            params=[actl_name, act_time, act_date, cat_name, act_comment])

        self.actl_id = self.timedb.get_logged_user_data(item='get_actl_id',\
            params=[actl_name, cat_name])

        self.eUi.show()

    def add_event(self):
        # Getting all info, entered by user.
        title = self.aUi.add_event_lineEdit_name.text()        
        category = self.aUi.add_event_comboBox_category.currentText()
        duration = self.aUi.add_event_lineEdit_time.text()
        date = self.aUi.add_event_dateEdit.date()
        comment = self.aUi.add_event_plaintextedit_comment.toPlainText()

        if title == '':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Пожалуйста, дайте название своему событию.',\
                    QtWidgets.QMessageBox.Ok)
            return
        elif category == '':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Пожалуйста, укажите категорию для своего события.',\
                    QtWidgets.QMessageBox.Ok)
            return
        elif duration == '':
            QtWidgets.QMessageBox.question(self, 'Ошибка!',\
                'Пожалуйста, укажите потраченное время на активность в минутах.',\
                    QtWidgets.QMessageBox.Ok)
            return

        date_ = datetime.date(date.year(), date.month(), date.day())
        str_date = date_.strftime('%Y-%m-%d')
        
        int_duration = int(''.join(filter(str.isdigit, duration)))

        # Writing all changes to db and closing 'Add Event' win.
        if not self.timedb.set_logged_user_data(item='check_event_data',\
            add_params=[category, title, int_duration, str_date, comment]) == True:
            self.timedb.set_logged_user_data(item='add_event',\
                add_params=[category, title, int_duration, str_date, comment])
        
        self.aUi.close()
        self.add_event_status = True 

        # self.timedb.update_user_activities(self.user_n_name)
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
        self.timedb.edit_event(self.user_n_name, title, int_duration,\
            str_date, category, comment, self.act_id, self.actl_id)
        self.eUi.close()
        self.edit_event_status = True

# ----------------------------------------------------------END----actions_ui.py

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainUI()
    sys.exit(app.exec())
    
    # dbl = DbLogic()
    # dbl.get_logged_user_data(user_login='test', item='set_working_user')

    # print(dbl.get_logged_user_data(item='get_user_categories'))
    # print(dbl.get_logged_user_data(item='get_act_id', params=['Кушал', 60, '2021-05-26', 'Еда', '1']))
    # print(dbl.get_logged_user_data(item='get_actl_id', params=['Еда', 'Кушал']))
    # print(dbl.get_logged_user_data(item='get_user_activities'))
    # print(dbl.get_logged_user_data(item='get_user_p_id'))
    # print(dbl.get_logged_user_data(item='get_user_email'))
    # print(dbl.get_logged_user_data(item='get_user_password'))
    


    # dbl.set_logged_user_data(user_login='test', item='set_working_user')

    # if not dbl.set_logged_user_data(item='check_event_data', add_params=['Еда', 'Кушал', 60, '2021-05-26', '1']) == True:
    # dbl.set_logged_user_data(item='add_event', add_params=['Еда', 'Кушал1', '60', '2021-05-26', '1'])
    # if not dbl.set_logged_user_data('test', 'check_event_data', ['Спорт', 'Бег', 300, '2021-05-27', 'ВАУ']) == True:
    #     dbl.set_logged_user_data('test', 'edit_event', ['Еда', 'Кушал1', 30, '2021-05-27', 'Не вкусно!'], \
    #         ['Еда', 'Кушал', 60, '2021-05-26', '1'])

    # dbl.set_logged_user_data('test', 'del_event', ['Спорт', 'Бег', 300, '2021-05-27', 'ВАУ'])
    # print(dbl.get_logged_user_data(item='get_user_activities'))
    # dbl.set_logged_user_data(item='del_event', add_params=['Спорт23', 'Бег23', 300, '2021-05-27', 'ВАУ'])
    # print(dbl.set_logged_user_data(item='check_event_data', add_params=['Еда', 'Кушал', 60, '2021-05-26', '1']))
    # print(dbl.set_logged_user_data(item='change_password', edit_params=['qwerty123', 'test@test.test']))