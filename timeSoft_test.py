import sys
from uuid import uuid4
import os
import re

import configparser
import datetime
import csv
import webbrowser
from datetime import datetime

# import pandas
from psycopg2 import Error
import psycopg2.extras
import psycopg2 as db
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QBrush, QIcon, QPainter, QPen, QPixmap
from PyQt5.QtCore import Qt
from pyqtgraph.graphicsItems.ButtonItem import ButtonItem

from pandas import read_csv
from matplotlib import pyplot as plt

from pandas import read_csv


sys.path.append(".")


class InputCheck:
    """
    This class implements base checking system for various input data.
    """

    def __init__(self, input_text):
        """
        Parameters:
            input_text (str):The string which can be checked using various methods.

        Returns:
            None
        """
        self.text = input_text

        self.correct_rus_vals = []
        for i in range(1040, 1104):
            self.correct_rus_vals.append(ord(chr(i)))

        # Список с кодами корректных сиволов a-z - и _.
        self.correct_vals = list(range(ord('a'), ord('z')+1))
        # self.correct_rus_vals = list(range(chr(1040), chr(1103))+1)
        self.correct_vals_with_num = list(range(ord('0'), ord('9')+1))
        self.correct_vals_with_num.extend(self.correct_vals)

        # todo: Проверить необходимость использования.
        # self.only_in_quotes_char = [ord('!'), ord(','), ord(':')]
        self.incorrect_vals = [ord('"'), ord('\''), ord(
            '/'), ord('\\'), ord(','), ord('--'), ord(';')]

    def check_email(self):
        """
        This method makes various checks for correct email. 
        This method does various checks for email. 
        If the email passes verification, it returns True(bool) only.
        If not passes, it returns list that contains two values:
        False(bool) and error message(str).

        Parameters:
            None

        Returns:
            True | [False | err_msg]
        """
        # Check for the number of "@" characters.
        if self.text.count('@') > 1 or self.text.count('@') == 0:
            return [False, 'Неверное количество знаков "@".']

        # Check for domain length.
        [name, domain] = self.text.split('@')
        if len(domain) < 3:
            return [False, 'Доменное имя короче 3 символов.']
        if len(domain) > 60:
            return [False, 'Доменное имя длиннее 60 символов.']
        if domain.count('.') == 0:
            return [False, 'Доменное имя не содержит точки.']

        # Domain check.
        includedomain = domain.split('.')
        self.correct_vals.extend([ord('-'), ord('_')])
        for k in includedomain:
            # Checking if there are empty substrings in the domain.
            if k == '':
                return [False, 'Доменное имя содержит пустую строку между точками.']
            # Checking if there are any illegal characters in substrings
            # of the domain.
            for n in k:
                if ord(n) not in self.correct_vals:
                    return [False, f'Недопустимый символ {n}']
            if (k[0] == '-') or (k[len(k)-1] == '-'):
                return [False, 'Доменное имя не может начинаться/заканчиваться знаком "-".']
        if len(name) > 60:
            return [False, 'Имя почты длиннее 60 символов.']

        # Add to the list of valid characters (; " ! : ,).
        self.correct_vals_with_num.extend(self.only_in_quotes_char)
        self.correct_vals_with_num.extend([ord('.'), ord(';'), ord('"')])
        # Checking for double quotes.
        if name.count('"') % 2 != 0:
            return [False, 'Непарные кавычки.']
        # Variables to track period and opening quotes.
        doubledot = False
        inquotes = False
        for k in name:
            if (k == '"'):
                inquotes = not inquotes
            if (ord(k) in self.only_in_quotes_char) and (inquotes == False):
                return [False, 'Недопустимый символ вне кавычек.']
            if ord(k) not in self.correct_vals_with_num:
                return [False, f'Недопустимый символ. "{k}"']
            # Checking for two points in a row.
            if (k == '.'):
                if doubledot == True:
                    return [False, 'Две точки в названии почты.']
                else:
                    doubledot = True
        return True

    def check_date(self):
        if re.match(r"^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$", self.text) or datetime.strptime(self.text, '%d.%m.%Y').year < 1900 or datetime.strptime(self.text, '%d.%m.%Y') > datetime.now():
            return [False, 'Неверный формат даты.']
        return True

    def check_len(self):
        if len(self.text) > 60:
            return [False, 'Длиннее 60 символов.']
        return True

    def check_comment_len(self):
        if len(self.text) > 500:
            return [False, 'Длиннее 500 символов.']
        return True

    def check_time_value(self):
        if 1 > self.text or self.text > 1440:
            return [False, 'Введено ошибочное количество потраченных минут.']
        return True

    def check_incorrect_vals(self):
        for i in self.text:
            if ord(i) in self.incorrect_vals:
                return [False, f'Недопустимый символ {i}.']
        return True

    def check_spaces_tabs(self):
        tabs_spaces = [' ', '    ']
        if self.text in tabs_spaces:
            return [False, 'Табуляция или пробел.']
        return True

    def number_only(self):
        self.incorrect_vals.extend(self.only_in_quotes_char)
        self.correct_vals.extend([ord('.'), ord(';'), ord('"')])
        self.correct_vals.extend(self.correct_rus_vals)
        for i in self.text:
            if ord(i) in self.correct_vals or ord(i) in self.incorrect_vals:
                return [False, 'Разрешено вводить только количество минут.']
        return True


class InputCheckWithDiags(QtWidgets.QMessageBox):
    def __init__(self, input_text=None):
        super().__init__()
        self.input_text = input_text
        self.setIcon(QtWidgets.QMessageBox.Information)
        self.setWindowIcon(QIcon('design\\img\\main\\favicon.png'))
        self.setWindowTitle('Ошибка!')
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)

    def simple_diag(self, err_txt):
        self.setWindowTitle('Внимание!')
        self.setText(err_txt)
        return self.exec()

    def check_password_len(self, err_txt):
        if len(self.input_text) < 8:
            self.setText(
                f'{err_txt}: Пароль должен состоять минимум из 8 символов.')
            self.exec()
            return False
        return True

    def check_email(self, err_txt):
        try:
            chck_email = InputCheck(self.input_text).check_email()
            if chck_email[0] == False:
                self.setText(f'{err_txt}: {chck_email[1]}')
                self.exec()
            return False
        except Exception:
            pass
        return True

    def check_len(self, err_txt):
        try:
            chck_len = InputCheck(self.input_text).check_len()
            if chck_len[0] == False:
                self.setText(f'{err_txt}: {chck_len[1]}')
                self.exec()
            return False
        except Exception:
            pass
        return True

    def check_incorrect_vals(self, err_txt):
        try:
            chck_incorrect_vals = InputCheck(
                self.input_text).check_incorrect_vals()
            if chck_incorrect_vals[0] == False:
                self.setText(f'{err_txt}: {chck_incorrect_vals[1]}')
                self.exec()
                return False
        except Exception:
            pass
        return True

    def check_spaces_tabs(self, err_txt):
        try:
            chck_spaces_tabs = InputCheck(self.input_text).check_spaces_tabs()
            if chck_spaces_tabs[0] == False:
                self.setText(f'{err_txt}: {chck_spaces_tabs[1]}')
                self.exec()
                return False
        except Exception:
            pass
        return True

    def check_number_only(self, err_txt):
        try:
            chck_number_only = InputCheck(self.input_text).number_only()
            if chck_number_only[0] == False:
                self.setText(f'{err_txt}: {chck_number_only[1]}')
                self.exec()
                return False
        except Exception:
            pass
        return True

# ----------------------------------------------------------START-----timeSoft
# class AlignDelegate(QtWidgets.QStyledItemDelegate):
#     '''
#     This class implements center positioning for icons in TableView widget
#     '''
#     def initStyleOption(self, option, index):
#         super().initStyleOption(option, index)
#         option.decorationSize = option.rect.size()


class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Creating database instance.
        self.timedb = DbLogic()

        # Loading UI interfaces.
        self.mUi = uic.loadUi('design\\MainWindow_d.ui')  # Main window ui.
        self.aUi = uic.loadUi('design\\add_event_d.ui')  # Add actions ui.
        self.eUi = uic.loadUi('design\\edit_event_d.ui')  # Edit actions ui.
        # Registration window ui.
        self.rUi = uic.loadUi('design\\register_d.ui')
        self.lUi = uic.loadUi('design\\login_d.ui')  # Login window ui.
        self.sUi = uic.loadUi('design\\settings_d.ui')  # Settings window ui.
        self.ttUi = uic.loadUi('design\\table.ui')  # Table ui.
        self.abUi = uic.loadUi('design\\about_us_d.ui')  # About us ui.

        # Widget for viewing various data.
        self.wUi = self.mUi.mainwindow_widget_view

        # Various settings for different UI elements, such as connecting
        # buttons to slots, setting menubars and status bar.
        self.pre_initUI()

        # Connect TableView with mouseClick.
        self.ttUi.tableW.doubleClicked.connect(self.get_current_row_tableview)

        # self.ttUi.tableW.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # When starting a program, first login UI appears.
        self.show_login()

    def pre_initUI(self):
        icon = QtGui.QIcon('design\\img\\main\\favicon.png')
        # Connecting buttons to slots.
        # Main UI.
        self.mUi.setFixedHeight(768)
        self.mUi.setFixedWidth(1280)
        self.mUi.mainwindow_btn_nav_add_act.clicked.connect(
            self.show_add_action)
        self.mUi.mainwindow_btn_settings.clicked.connect(self.settings)
        self.mUi.mainwindow_btn_exit.clicked.connect(self.mUi.close)
        # Combobox.
        self.mUi.mainwindow_comboBox_display_style.currentIndexChanged.connect(
            self.graph_plot)
        # Theme of main window.
        self.mUi.mainwindow_btn_theme.clicked.connect(self.change_theme)
        self.change_theme_status = 0  # 0 is a sign of dark theme.

        self.mUi.setWindowIcon(icon)

        # Login UI.
        self.lUi.setFixedHeight(768)
        self.lUi.setFixedWidth(1280)
        self.lUi.login_btn_login.clicked.connect(self.login)
        self.lUi.login_btn_create_account.clicked.connect(
            self.show_registration)
        self.lUi.setWindowIcon(icon)

        # Register UI.
        self.rUi.setFixedHeight(768)
        self.rUi.setFixedWidth(1280)
        self.rUi.register_btn_login.clicked.connect(self.registration)
        self.rUi.register_btn_create.clicked.connect(self.show_login)
        self.rUi.setWindowIcon(icon)

        # Add event UI.
        self.aUi.setFixedHeight(640)
        self.aUi.setFixedWidth(360)
        self.aUi.add_event_btn_add.clicked.connect(self.add_action)
        self.aUi.add_event_btn_cancel.clicked.connect(self.aUi.close)
        self.aUi.add_event_btn_exit.clicked.connect(self.aUi.close)

        # Edit event UI.
        self.eUi.setFixedHeight(640)
        self.eUi.setFixedWidth(360)
        self.eUi.edit_event_btn_save.clicked.connect(self.edit_action)
        self.eUi.edit_event_btn_del.clicked.connect(self.delete_action)
        self.eUi.edit_event_btn_exit.clicked.connect(self.eUi.close)

        # Settings UI.
        self.sUi.setFixedHeight(768)
        self.sUi.setFixedWidth(1280)
        self.sUi.settings_btn_export.clicked.connect(self.settings_export)
        self.sUi.settings_btn_import.clicked.connect(self.settings_import)
        self.sUi.settings_btn_undo.clicked.connect(self.sUi.close)
        self.sUi.settings_btn_telegram.clicked.connect(self.settings_telegram)
        self.sUi.setWindowIcon(icon)

        # About us UI.
        self.abUi.setFixedHeight(768)
        self.abUi.setFixedWidth(1280)
        self.abUi.setWindowIcon(icon)

        # Menubar Main UI.
        self.mUi.mainwindow_act_exit.triggered.connect(self.mUi.close)
        self.mUi.mainwindow_act_settings.triggered.connect(self.settings)
        self.mUi.mainwindow_act_about_program.triggered.connect(self.abUi.show)

        # Forecast.
        self.mUi.mainwindow_btn_forecast.clicked.connect(self.forecast)

        # Layout creation and appending widget for viewing various data to it.
        self.lay = QtWidgets.QHBoxLayout()
        self.wUi.setLayout(self.lay)

        # Variable of correctness login status for bot.
        self.correct_login = False

        self.input_check = InputCheckWithDiags

    def sorting_data_csv(self):
        if self.idx < len(self.diff_categories):
            with open(f'./csv_data/{self.user_n_name}_{self.diff_categories[self.idx]}_data.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Month', 'Duration'])
                for item in self.duration_by_dates_and_categories:
                    if item['category'] == self.diff_categories[self.idx]:
                        print(item)
                        writer.writerow([item['date'], item['duration']])
            print('---')
            self.idx += 1
            self.sorting_data_csv()
        else:
            print('all data sorted by month and category successfully!')
        # For various checks.

    def post_initUI(self):
        self.user_id = self.timedb.get_logged_user_data(
            user_login=self.user_n_name, item='set_working_user')
        self.timedb.set_logged_user_data(
            user_login=self.user_n_name, item='set_working_user')
        self.timedb.get_logged_user_data(item='get_user_p_id')
        self.sUi.settings_lineedit_email.setText(
            self.timedb.get_logged_user_data(item='get_user_email'))
        if not self.timedb.get_logged_user_data(
                item='get_user_telegram') == '0' and not self.timedb.get_logged_user_data(
                item='get_user_telegram') == 'None':
            self.sUi.settings_imglbl_telegram_noverify.setHidden(True)
        self.update_users_categs()

    def create_forecast_data(self):
        self.graph_plot()
        rows = self.timedb.get_logged_user_data(item='get_user_activities')
        self.dates = []

        for row in rows:
            self.dates.append(row[3][0:-3])
            # self.dates.append(row[3][0:-3])
        self.diff_dates = list(
            (set([x for x in self.dates if self.dates.count(x) > 1])))

        self.sorted_diff_dates = sorted(
            self.diff_dates, key=lambda x: datetime.datetime.strptime(x, '%Y-%m'))

        self.final_date = []
        self.final_category = []
        self.final_duration = []

        for i in self.sorted_diff_dates:
            for row in rows:
                for j in self.diff_categories:
                    if i == row[3][0:-3] and j == row[0]:
                        self.final_date.append(i)
                        self.final_category.append(j)
                        self.final_duration.append(int(row[2]))

        self.duration_by_dates_and_categories = []
        self.sum_of_durations = 0
        self.case = dict

        for i in self.sorted_diff_dates:  # dates.
            for j in self.diff_categories:  # categories.
                # number of all dates in order.
                for z in range(len(self.final_date)):
                    if i == self.final_date[z] and j == self.final_category[z]:
                        self.sum_of_durations += self.final_duration[z]
                self.case = {'date': i, 'category': j,
                             'duration': self.sum_of_durations}
                self.duration_by_dates_and_categories.append(self.case)
                # self.case.clear()
                self.sum_of_durations = 0

        # print(self.duration_by_dates_and_categories)

        # Looping through dicts in list.
        # self.categories_range = range(len(self.diff_categories))

        # categories_range = range(len(self.diff_categories))
        # dates_len = len(self.diff_dates)
        # idx = 0
        # for item in self.duration_by_dates_and_categories:
        #     for i in categories_range:
        #         if item['category'] == self.diff_categories[i] and item['date'] == self.diff_dates[idx] and idx <= dates_len:
        #             print(item)
        # idx+=1

        # print(f'\n{self.final_date}\n{self.final_category}\n{self.final_duration}')
        # print(self.dates, self.diff_categories, self.diff_duration)
        # for i in diff_categ

        # with open(f'./csv_data/{self.user_n_name}_data.csv', 'w', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerow(['Month', 'Category', 'Duration'])

            # for i in
        # self.diff_categories = list((set([x for x in self.categories if self.categories.count(x) > 1])))

        print(self.dates, self.diff_categories, self.diff_duration)

        with open(f'{self.user_n_name}_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Month', 'Category', 'Duration'])
            # for i in
            # writer.writerow([1, "Potato", "Linux Kernel"])
            # writer.writerow([2, "Tim Berners-Lee", "World Wide Web"])
            # writer.writerow([3, "Guido van Rossum", "Python Programming"])

    def forecast(self):
        self.idx = 0  # Setting index to 0.
        self.sorting_data_csv()

        # load data.
        index = 0
        pathes = []

        for i in range(len(self.diff_categories)):
            path = f'./csv_data/{self.user_n_name}_{self.diff_categories[index]}_data.csv'
            pathes.append(path)
            # plot the time series.
            df = read_csv(pathes[i])
            df.plot(subplots=True)
            # df.plot(subplots=True, legend = True)
            index += 1
        plt.show()

    # TODO: ADD STYLES.
    def change_theme(self):
        if self.change_theme_status == 0:
            # print('white theme')

            # self.mUi.mainwindow.setStyleSheet("""style""")
            self.mUi.setStyleSheet("""
            background-color: #F8F8F8;
            """)
            self.mUi.mainwindow_widget_category.setStyleSheet("""
            QWidget { \nbackground-color: rgb(255, 255, 255);\nborder-top-left-radius: 5px;\nborder-bottom-left-radius: 5px;\n}
            """)
            self.mUi.mainwindow_checkBox_entertainment.setStyleSheet("""
            QCheckBox {\ncolor: #5E5873;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQCheckBox:hover {\ncolor: #5E5873;\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}
            """)
            self.mUi.mainwindow_checkBox_family.setStyleSheet("""
            QCheckBox {\ncolor: #5E5873;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQCheckBox:hover {\ncolor: #5E5873;\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}
            """)
            self.mUi.mainwindow_checkBox_health.setStyleSheet("""
            QCheckBox {\ncolor: #5E5873;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQCheckBox:hover {\ncolor: #5E5873;\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}
            """)
            self.mUi.mainwindow_checkBox_relaxation.setStyleSheet("""
            QCheckBox {\ncolor: #5E5873;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQCheckBox:hover {\ncolor: #5E5873;\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}
            """)
            self.mUi.mainwindow_checkBox_see_all.setStyleSheet("""
            QCheckBox {\ncolor: #5E5873;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQCheckBox:hover {\ncolor: #5E5873;\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}
            """)
            self.mUi.mainwindow_checkBox_work.setStyleSheet("""
            QCheckBox {\ncolor: #5E5873;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQCheckBox:hover {\ncolor: #5E5873;\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}
            """)
            self.mUi.mainwindow_checkBoxlbl_dinamic.setStyleSheet("""
            QLabel {\ncolor: #5E5873;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQLabel:hover {\ncolor: #5E5873;\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}
            """)
            self.mUi.mainwindow_lbl_time_all.setStyleSheet("""
            QLabel {\ncolor: #5E5873;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQLabel:hover {\ncolor: #5E5873;\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}
            """)
            self.mUi.mainwindow_lbl_time_dinamic.setStyleSheet("""
            QLabel {\ncolor: #5E5873;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQLabel:hover {\ncolor: #5E5873;\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}
            """)
            self.mUi.mainwindow_lbl_time_entertainment.setStyleSheet("""
            QLabel {\ncolor: #5E5873;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQLabel:hover {\ncolor: #5E5873;\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}
            """)
            self.mUi.mainwindow_lbl_time_family.setStyleSheet("""
            QLabel {\ncolor: #5E5873;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQLabel:hover {\ncolor: #5E5873;\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}
            """)
            self.mUi.mainwindow_lbl_time_health.setStyleSheet("""
            QLabel {\ncolor: #5E5873;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQLabel:hover {\ncolor: #5E5873;\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}
            """)
            self.mUi.mainwindow_lbl_time_relaxation.setStyleSheet("""
            QLabel {\ncolor: #5E5873;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQLabel:hover {\ncolor: #5E5873;\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}
            """)
            self.mUi.mainwindow_lbl_time_work.setStyleSheet("""
            QLabel {\ncolor: #5E5873;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQLabel:hover {\ncolor: #5E5873;\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}
            """)
            self.mUi.mainwindow_textlbl_category.setStyleSheet("""
            color: #B9B9C3;\nborder: 2px solid rgba(0, 0, 0, 0);\nmargin-top: 2px;
            """)
            self.mUi.mainwindow_widget_navigation.setStyleSheet("""
            QWidget { \nbackground-color: #FFFFFF;\nborder-radius: 5px;\n}
            """)
            self.mUi.mainwindow_btn_annually.setStyleSheet("""
            QPushButton {\n	color: #7367F0;\n	border: 2px solid rgb(95, 85, 200);\n	border-top-left-radius: 0px;\n	border-top-right-radius: 5px;\n	border-bottom-right-radius: 5px;\n	border-bottom-left-radius: 0px;\n	padding-left: 20px;\n	padding-right: 20px;\n}\nQPushButton:hover {\n	background-color: rgba(104, 93, 216, 0.2); \n	color: #7367F0;\n	border: 2px solid rgb(121, 109, 255);\n	border-top-left-radius: 0px;\n	border-top-right-radius: 5px;\n	border-bottom-right-radius: 5px;\n	border-bottom-left-radius: 0px;\n}
            """)
            self.mUi.mainwindow_btn_daily.setStyleSheet("""
            QPushButton {\n	color: #7367F0;\n	border: 2px solid rgb(95, 85, 200);\n	border-right: 0px;\n	border-top-left-radius: 5px;\n	border-top-right-radius: 0px;\n	border-bottom-right-radius: 0px;\n	border-bottom-left-radius: 5px;\n	padding-left: 20px;\n	padding-right: 20px;\n}\nQPushButton:hover {\n	background-color: rgba(104, 93, 216, 0.2); \n	color: #7367F0;\n	border: 2px solid rgb(121, 109, 255);\n	border-top-left-radius: 5px;\n	border-top-right-radius: 0px;\n	border-bottom-right-radius: 0px;\n	border-bottom-left-radius: 5px;\n}
            """)
            self.mUi.mainwindow_btn_monthly.setStyleSheet("""
            QPushButton {\n	color: #7367F0;\n	border: 2px solid rgb(95, 85, 200);\n	border-right: 0px;\n	border-radius: 0;\n	padding-left: 20px;\n	padding-right: 20px;\n}\nQPushButton:hover {\n	background-color: rgba(104, 93, 216, 0.2); \n	color: #7367F0;\n	border: 2px solid rgb(121, 109, 255);\n	border-radius: 0;\n}
            """)
            self.mUi.mainwindow_btn_nav_add_act.setStyleSheet("""
            QPushButton {\n	background-color: rgb(115, 103, 240);\n	color: rgb(255, 255, 255);\n	border: 2px solid rgb(115, 103, 240);\n	border-radius: 5px;\n	padding-left: 12px;\n	padding-right: 12px;\n	padding-top: 5px;\n	padding-bottom: 5px;\n}\nQPushButton:hover {\n	background-color: rgba(0, 0, 0, 0);\n	color: rgb(94, 88, 115);\n	border: 2px solid rgb(115, 103, 240);\n}
            """)
            self.mUi.mainwindow_btn_weekly.setStyleSheet("""
            QPushButton {\n	color: #7367F0;\n	border: 2px solid rgb(95, 85, 200);\n	border-right: 0px;\n	border-radius: 0;\n	padding-left: 20px;\n	padding-right: 20px;\n}\nQPushButton:hover {\n	background-color: rgba(104, 93, 216, 0.2); \n	color: #7367F0;\n	border: 2px solid rgb(121, 109, 255);\n	border-radius: 0;\n}
            """)
            self.mUi.mainwindow_dateEdit_po.setStyleSheet("""
            /* QDateEdit {\n	background-color: rgb(255, 255, 255);\n	border-radius: 5px;\n	color: #5E5873;\n}\nQDateEdit:hover {\n	background-color: rgb(248, 248, 248); \n	color: #5E5873;\n}\n*/\nQDateEdit {\n	background-color: rgb(248, 248, 248);\n	border-radius: 5px;\n	color: #5E5873;\n}\nQDateEdit:hover {\n	background-color: rgb(230, 230, 230);\n	color: #5E5873;\n}
            """)
            self.mUi.mainwindow_dateEdit_s.setStyleSheet("""
            QDateEdit {\n	background-color: rgb(248, 248, 248);\n	border-radius: 5px;\n	color: #5E5873;\n}\nQDateEdit:hover {\n	background-color: rgb(230, 230, 230);\n	color: #5E5873;\n}
            """)
            self.mUi.mainwindow_lbl_icon_clendar.setStyleSheet("""
            margin-left: 30px;\ncolor: #D0D2D6;\npadding-top: 4px;\npadding-bottom: 4px;
            """)
            self.mUi.mainwindow_textlbl_po.setStyleSheet("""
            padding-left: 5px;\npadding-right: 5px;\ncolor: #6E6B7B;
            """)
            self.mUi.mainwindow_textlbl_s.setStyleSheet("""
            padding-left: 5px;\npadding-right: 5px;\ncolor: #6E6B7B;
            """)
            self.mUi.mainwindow_widget_view.setStyleSheet("""
            background-color: #283046;\nbackground-image: url(design/img/background-image_d.png);\ncolor: rgb(110, 107, 123);\nborder-top-right-radius: 5px;\nborder-bottom-right-radius: 5px;\n
            """)
            self.mUi.mainwindow_widget_view_spacer.setStyleSheet("""
            border-right: 1px solid #EBE9F1;\nbackground-color: #FFFFFF;
            """)
            self.mUi.mainwindow_widget_logo.setStyleSheet("""
            background-color: rgb(255, 255, 255);
            """)
            self.mUi.mainwindow_lbl_logo_title.setStyleSheet("""
            color: #7367F0;
            """)
            self.mUi.mainwindow_widget_menu.setStyleSheet("""
            background-color: rgb(255, 255, 255);
            """)
            self.mUi.mainwindow_btn_exit.setStyleSheet("""
            QPushButton {\n	background-color: rgba(0, 0, 0, 0);	\n	color: #5E5873;\n	text-align: left;\n	padding-right: 10px;\n}\nQPushButton:hover {\n	background-color: rgba(0, 0, 0, 0);  \n	color: #7367F0;\n}
            """)
            self.mUi.mainwindow_btn_forecast.setStyleSheet("""
            QPushButton {\n	background-color: rgba(0, 0, 0, 0);	\n	color: #5E5873;\n	text-align: left;\n	padding-right: 10px;\n	margin-top: 27px;\n}\nQPushButton:hover {\n	background-color: rgba(0, 0, 0, 0);  \n	color: #7367F0;\n}
            """)
            self.mUi.mainwindow_btn_settings.setStyleSheet("""
            QPushButton {\n	background-color: rgba(0, 0, 0, 0);	\n	color: #5E5873;\n	text-align: left;\n	padding-right: 10px;\n}\nQPushButton:hover {\n	background-color: rgba(0, 0, 0, 0);  \n	color: #7367F0;\n}
            """)
            self.mUi.mainwindow_btn_theme.setStyleSheet("""
            QPushButton {\n	background-color: rgba(0, 0, 0, 0);	\n	color: #5E5873;\n	text-align: left;\n	padding-right: 10px;\n}\nQPushButton:hover {\n	background-color: rgba(0, 0, 0, 0);  \n	color: #7367F0;\n}
            """)
            self.mUi.mainwindow_comboBox_display_style.setStyleSheet("""
            QComboBox {\nbackground-color: rgb(248, 248, 248);\ncolor: rgb(94, 88, 115);\nborder: 2px solid rgba(0, 0, 0, 0);\nborder-radius: 5px;\npadding-left: 10px;\npadding-right: 10px;\n}\n\nQComboBox:hover {\nbackground-color: rgb(230, 230, 230);\ncolor: rgb(94, 88, 115);\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}\n\nQComboBox QAbstractItemView {\nbackground-color: rgb(230, 230, 230);\nborder: 2px solid #7666F8;\ncolor: rgb(94, 88, 115);\nselection-background-color: rgb(94, 80, 238);\nselection-color: rgb(0, 0, 0);\n}
            """)
            self.mUi.mainwindow_textlbl_display_style.setStyleSheet("""
            color: rgb(94, 88, 115);\nmargin-top: 20px;
            """)
            self.mUi.mainwindow_menubar.setStyleSheet("""
            QMenuBar {\n	color: rgb(205, 205, 205);	\n	background-color: rgba(0, 0, 0, 130);\n}\nQMenuBar::item:selected { \n	background-color: rgb(200, 200, 200);\n	color: rgb(0, 0, 0);\n} \nQMenuBar::item:pressed {  \n	background-color: rgb(200, 200, 200);\n	color: rgb(0, 0, 0);\n}
            """)
            self.mUi.mainwindow_menuFile.setStyleSheet("""
            QMenu {\n	background-color: rgb(20, 24, 34);\n	color: rgb(205, 205, 205);\n}\nQMenu::item:selected { \n	background-color: rgb(200, 200, 200);\n	color: rgb(0, 0, 0);\n} \nQMenu::item:pressed {  \n	background-color: rgb(200, 200, 200);\n	color: rgb(0, 0, 0);\n}
            """)
            self.mUi.mainwindow_menuEdit.setStyleSheet("""
            QMenu {\n	background-color: rgb(20, 24, 34);\n	color: rgb(205, 205, 205);\n}\nQMenu::item:selected { \n	background-color: rgb(200, 200, 200);\n	color: rgb(0, 0, 0);\n} \nQMenu::item:pressed {  \n	background-color: rgb(200, 200, 200);\n	color: rgb(0, 0, 0);\n}
            """)
            self.mUi.mainwindow_dropdown_menu_select_chart.setStyleSheet("""
            QMenu {\n	background-color: rgb(20, 24, 34);\n	color: rgb(205, 205, 205);\n}\nQMenu::item:selected { \n	background-color: rgb(200, 200, 200);\n	color: rgb(0, 0, 0);\n} \nQMenu::item:pressed {  \n	background-color: rgb(200, 200, 200);\n	color: rgb(0, 0, 0);\n}
            """)
            self.mUi.mainwindow_menuHelp.setStyleSheet("""
            QMenu {\n	background-color: rgb(20, 24, 34);\n	color: rgb(205, 205, 205);\n}\nQMenu::item:selected { \n	background-color: rgb(200, 200, 200);\n	color: rgb(0, 0, 0);\n} \nQMenu::item:pressed {  \n	background-color: rgb(200, 200, 200);\n	color: rgb(0, 0, 0);\n}
            """)

            self.change_theme_status = 1

        else:
            # print('dark theme')

            self.mUi.setStyleSheet("""background-color: #161D31;""")
            self.mUi.mainwindow_widget_category.setStyleSheet(
                """QWidget { \nbackground-color: #283046;\nborder-top-left-radius: 5px;\nborder-bottom-left-radius: 5px;\n}""")
            self.mUi.mainwindow_checkBox_entertainment.setStyleSheet(
                """QCheckBox {\ncolor: #B4B7BD;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQCheckBox:hover {\nbackground-color: rgb(40, 48, 70);\ncolor: rgb(185, 185, 195);\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}""")
            self.mUi.mainwindow_checkBox_family.setStyleSheet(
                """QCheckBox {\ncolor: #B4B7BD;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQCheckBox:hover {\nbackground-color: rgb(40, 48, 70);\ncolor: rgb(185, 185, 195);\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}""")
            self.mUi.mainwindow_checkBox_health.setStyleSheet(
                """QCheckBox {\ncolor: #B4B7BD;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQCheckBox:hover {\nbackground-color: rgb(40, 48, 70);\ncolor: rgb(185, 185, 195);\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}""")
            self.mUi.mainwindow_checkBox_relaxation.setStyleSheet(
                """QCheckBox {\ncolor: #B4B7BD;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQCheckBox:hover {\nbackground-color: rgb(40, 48, 70);\ncolor: rgb(185, 185, 195);\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}""")
            self.mUi.mainwindow_checkBox_see_all.setStyleSheet(
                """QCheckBox {\ncolor: #B4B7BD;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQCheckBox:hover {\nbackground-color: rgb(40, 48, 70);\ncolor: rgb(185, 185, 195);\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}""")
            self.mUi.mainwindow_checkBox_work.setStyleSheet(
                """QCheckBox {\ncolor: #B4B7BD;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQCheckBox:hover {\nbackground-color: rgb(40, 48, 70);\ncolor: rgb(185, 185, 195);\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}""")
            self.mUi.mainwindow_checkBoxlbl_dinamic.setStyleSheet(
                """QLabel {\ncolor: #B4B7BD;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQLabel:hover {\nbackground-color: rgb(40, 48, 70);\ncolor: rgb(185, 185, 195);\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}""")
            self.mUi.mainwindow_lbl_time_all.setStyleSheet(
                """QLabel {\ncolor: #B4B7BD;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQLabel:hover {\nbackground-color: rgb(40, 48, 70);\ncolor: rgb(185, 185, 195);\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}""")
            self.mUi.mainwindow_lbl_time_dinamic.setStyleSheet(
                """QLabel {\ncolor: #B4B7BD;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQLabel:hover {\nbackground-color: rgb(40, 48, 70);\ncolor: rgb(185, 185, 195);\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}""")
            self.mUi.mainwindow_lbl_time_entertainment.setStyleSheet(
                """QLabel {\ncolor: #B4B7BD;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQLabel:hover {\nbackground-color: rgb(40, 48, 70);\ncolor: rgb(185, 185, 195);\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}""")
            self.mUi.mainwindow_lbl_time_family.setStyleSheet(
                """QLabel {\ncolor: #B4B7BD;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQLabel:hover {\nbackground-color: rgb(40, 48, 70);\ncolor: rgb(185, 185, 195);\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}""")
            self.mUi.mainwindow_lbl_time_health.setStyleSheet(
                """QLabel {\ncolor: #B4B7BD;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQLabel:hover {\nbackground-color: rgb(40, 48, 70);\ncolor: rgb(185, 185, 195);\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}""")
            self.mUi.mainwindow_lbl_time_relaxation.setStyleSheet(
                """QLabel {\ncolor: #B4B7BD;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQLabel:hover {\nbackground-color: rgb(40, 48, 70);\ncolor: rgb(185, 185, 195);\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}""")
            self.mUi.mainwindow_lbl_time_work.setStyleSheet(
                """QLabel {\ncolor: #B4B7BD;\nborder: 2px solid rgba(0, 0, 0, 0) ;\n}\n\nQLabel:hover {\nbackground-color: rgb(40, 48, 70);\ncolor: rgb(185, 185, 195);\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}""")
            self.mUi.mainwindow_textlbl_category.setStyleSheet(
                """color: #B4B7BD;\nborder: 2px solid rgba(0, 0, 0, 0);\nmargin-top: 2px;""")
            self.mUi.mainwindow_widget_navigation.setStyleSheet(
                """QWidget { \nbackground-color: #283046;\nborder-radius: 5px;\n}""")
            self.mUi.mainwindow_btn_annually.setStyleSheet("""QPushButton {\n	background-color: #283046;\n	color: #FFFFFF;\n	border: 2px solid rgb(95, 85, 200);\n	border-top-left-radius: 0px;\n	border-top-right-radius: 5px;\n	border-bottom-right-radius: 5px;\n	border-bottom-left-radius: 0px;\n	padding-left: 20px;\n	padding-right: 20px;\n}\nQPushButton:hover {\n	background-color: rgb(40, 48, 70); \n	color: rgb(255, 255, 255);\n	border: 2px solid rgb(121, 109, 255);\n	border-top-left-radius: 0px;\n	border-top-right-radius: 5px;\n	border-bottom-right-radius: 5px;\n	border-bottom-left-radius: 0px;\n}""")
            self.mUi.mainwindow_btn_daily.setStyleSheet("""QPushButton {\n	background-color: #283046;\n	color: #FFFFFF;\n	border: 2px solid rgb(95, 85, 200);\n	border-right: 0px;\n	border-top-left-radius: 5px;\n	border-top-right-radius: 0px;\n	border-bottom-right-radius: 0px;\n	border-bottom-left-radius: 5px;\n	padding-left: 20px;\n	padding-right: 20px;\n}\nQPushButton:hover {\n	background-color: rgb(40, 48, 70); \n	color: rgb(255, 255, 255);\n	border: 2px solid rgb(121, 109, 255);\n	border-top-left-radius: 5px;\n	border-top-right-radius: 0px;\n	border-bottom-right-radius: 0px;\n	border-bottom-left-radius: 5px;\n}""")
            self.mUi.mainwindow_btn_monthly.setStyleSheet(
                """QPushButton {\n	background-color: #283046;\n	color: #FFFFFF;\n	border: 2px solid rgb(95, 85, 200);\n	border-right: 0px;\n	border-radius: 0;\n	padding-left: 20px;\n	padding-right: 20px;\n}\nQPushButton:hover {\n	background-color: rgb(40, 48, 70); \n	color: rgb(255, 255, 255);\n	border: 2px solid rgb(121, 109, 255);\n	border-radius: 0;\n}""")
            self.mUi.mainwindow_btn_nav_add_act.setStyleSheet(
                """QPushButton {\n	background-color: rgb(115, 103, 240);\n	color: rgb(255, 255, 255);\n	border: 2px solid rgb(115, 103, 240);\n	border-radius: 5px;\n	padding-left: 12px;\n	padding-right: 12px;\n	padding-top: 5px;\n	padding-bottom: 5px;\n}\nQPushButton:hover {\n	background-color: rgba(0, 0, 0, 0);\n	color: rgb(115, 103, 240);\n	border: 2px solid rgb(115, 103, 240);\n}""")
            self.mUi.mainwindow_btn_weekly.setStyleSheet(
                """QPushButton {\n	background-color: #283046;\n	color: #FFFFFF;\n	border: 2px solid rgb(95, 85, 200);\n	border-right: 0px;\n	border-radius: 0;\n	padding-left: 20px;\n	padding-right: 20px;\n}\nQPushButton:hover {\n	background-color: rgb(40, 48, 70); \n	color: rgb(255, 255, 255);\n	border: 2px solid rgb(121, 109, 255);\n	border-radius: 0;\n}""")
            self.mUi.mainwindow_dateEdit_po.setStyleSheet(
                """QDateEdit {\n	background-color: #283046;\n	border-radius: 5px;\n	color: rgb(255, 255, 255);\n}\nQDateEdit:hover {\n	background-color: rgb(40, 48, 70); \n	color: rgb(255, 255, 255);\n}""")
            self.mUi.mainwindow_dateEdit_s.setStyleSheet(
                """QDateEdit {\n	background-color: #283046;\n	border-radius: 5px;\n	color: rgb(255, 255, 255);\n}\nQDateEdit:hover {\n	background-color: rgb(40, 48, 70); \n	color: rgb(255, 255, 255);\n}""")
            self.mUi.mainwindow_lbl_icon_clendar.setStyleSheet(
                """margin-left: 30px;\ncolor: #D0D2D6;\npadding-top: 4px;\npadding-bottom: 4px;""")
            self.mUi.mainwindow_textlbl_po.setStyleSheet(
                """padding-left: 5px;\npadding-right: 5px;\ncolor: #D0D2D6;""")
            self.mUi.mainwindow_textlbl_s.setStyleSheet(
                """padding-left: 5px;\npadding-right: 5px;\ncolor: #D0D2D6;""")
            self.mUi.mainwindow_widget_view.setStyleSheet(
                """background-color: #283046;\nbackground-image: url(design/img/background-image_d.png);\nborder-top-right-radius: 5px;\nborder-bottom-right-radius: 5px;\n""")
            self.mUi.mainwindow_widget_view_spacer.setStyleSheet(
                """border-right: 1px solid #3B4253;\nbackground-color: #283046;""")
            self.mUi.mainwindow_widget_logo.setStyleSheet(
                """background-color: #283046;""")
            self.mUi.mainwindow_lbl_logo_title.setStyleSheet(
                """color: #7367F0;""")
            self.mUi.mainwindow_widget_menu.setStyleSheet(
                """background-color: #283046;""")
            self.mUi.mainwindow_btn_exit.setStyleSheet(
                """QPushButton {\n	background-color: rgba(0, 0, 0, 0);	\n	color: rgb(208, 210, 214);\n	text-align: left;\n	padding-right: 10px;\n}\nQPushButton:hover {\n	background-color: rgba(0, 0, 0, 0);  \n	color: rgb(95, 85, 200);\n}""")
            self.mUi.mainwindow_btn_forecast.setStyleSheet(
                """QPushButton {\n	background-color: rgba(0, 0, 0, 0);	\n	color: rgb(208, 210, 214);\n	text-align: left;\n	padding-right: 10px;\n	margin-top: 27px;\n}\nQPushButton:hover {\n	background-color: rgba(0, 0, 0, 0);  \n	color: rgb(95, 85, 200);\n}""")
            self.mUi.mainwindow_btn_settings.setStyleSheet(
                """QPushButton {\n	background-color: rgba(0, 0, 0, 0);	\n	color: rgb(208, 210, 214);\n	text-align: left;\n	padding-right: 10px;\n}\nQPushButton:hover {\n	background-color: rgba(0, 0, 0, 0);  \n	color: rgb(95, 85, 200);\n}""")
            self.mUi.mainwindow_btn_theme.setStyleSheet(
                """QPushButton {\n	background-color: rgba(0, 0, 0, 0);	\n	color: rgb(208, 210, 214);\n	text-align: left;\n	padding-right: 10px;\n}\nQPushButton:hover {\n	background-color: rgba(0, 0, 0, 0);  \n	color: rgb(95, 85, 200);\n}""")
            self.mUi.mainwindow_comboBox_display_style.setStyleSheet(
                """QComboBox {\nbackground-color: rgb(22, 29, 49);\ncolor: rgb(208, 210, 214);\nborder: 2px solid rgba(0, 0, 0, 0);\nborder-radius: 5px;\npadding-left: 10px;\npadding-right: 10px;\n}\n\nQComboBox:hover {\nbackground-color: rgb(40, 48, 70);\ncolor: rgb(185, 185, 195);\nborder: 2px solid #7666F8;\nborder-radius: 5px;\n}\n\nQComboBox QAbstractItemView {\nbackground-color: rgb(22, 29, 49);\nborder: 2px solid #7666F8;\ncolor: rgb(203, 203, 203);\nselection-background-color: rgb(94, 80, 238);\nselection-color: rgb(0, 0, 0);\n}""")
            self.mUi.mainwindow_textlbl_display_style.setStyleSheet(
                """color: #D0D2D6;\nmargin-top: 20px;""")
            self.mUi.mainwindow_menubar.setStyleSheet(
                """stQMenuBar {\n	color: rgb(205, 205, 205);	\n	background-color: rgba(0, 0, 0, 130);\n}\nQMenuBar::item:selected { \n	background-color: rgb(200, 200, 200);\n	color: rgb(0, 0, 0);\n} \nQMenuBar::item:pressed {  \n	background-color: rgb(200, 200, 200);\n	color: rgb(0, 0, 0);\n}le""")
            self.mUi.mainwindow_menuFile.setStyleSheet(
                """QMenu {\n	background-color: rgb(20, 24, 34);\n	color: rgb(205, 205, 205);\n}\nQMenu::item:selected { \n	background-color: rgb(200, 200, 200);\n	color: rgb(0, 0, 0);\n} \nQMenu::item:pressed {  \n	background-color: rgb(200, 200, 200);\n	color: rgb(0, 0, 0);\n}""")
            self.mUi.mainwindow_menuEdit.setStyleSheet(
                """QMenu {\n	background-color: rgb(20, 24, 34);\n	color: rgb(205, 205, 205);\n}\nQMenu::item:selected { \n	background-color: rgb(200, 200, 200);\n	color: rgb(0, 0, 0);\n} \nQMenu::item:pressed {  \n	background-color: rgb(200, 200, 200);\n	color: rgb(0, 0, 0);\n}""")
            self.mUi.mainwindow_dropdown_menu_select_chart.setStyleSheet(
                """QMenu {\n	background-color: rgb(20, 24, 34);\n	color: rgb(205, 205, 205);\n}\nQMenu::item:selected { \n	background-color: rgb(200, 200, 200);\n	color: rgb(0, 0, 0);\n} \nQMenu::item:pressed {  \n	background-color: rgb(200, 200, 200);\n	color: rgb(0, 0, 0);\n}""")
            self.mUi.mainwindow_menuHelp.setStyleSheet(
                """QMenu {\n	background-color: rgb(20, 24, 34);\n	color: rgb(205, 205, 205);\n}\nQMenu::item:selected { \n	background-color: rgb(200, 200, 200);\n	color: rgb(0, 0, 0);\n} \nQMenu::item:pressed {  \n	background-color: rgb(200, 200, 200);\n	color: rgb(0, 0, 0);\n}""")

            self.change_theme_status = 0

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

        if login == '':
            self.input_check().simple_diag(
                'Строка логина пуста. Пожалуйста, введите Ваш логин.')
            return

        if password == '':
            self.input_check().simple_diag(
                'Строка с паролем пуста. Пожалуйста, введите Ваш пароль.')
            return

        self.timedb.login_user(login, password)

        if self.timedb.correct_login_info == False:
            self.input_check().simple_diag('Неверный логин или пароль!')

        elif self.timedb.correct_login_info == True:
            self.user_n_name = login
            self.post_initUI()
            self.lUi.close()
            self.mUi.show()
            self.custom_view_table_test()  # Viewing table.
            self.correct_login = True
            self.create_forecast_data()  # Forcast data creation

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

        # Login checks.
        if login == '':
            self.input_check().simple_diag(
                'Нельзя создать пустой логин пользователя.')
            return
        elif self.input_check(login).check_incorrect_vals('Логин') == False:
            return
        elif self.input_check(login).check_len('Логин') == False:
            return
        elif self.input_check(login).check_spaces_tabs('Логин') == False:
            return

        # Email checks.
        if email == '':
            self.input_check().simple_diag(
                'Нельзя создать пустой email пользователя.')
            return
        elif self.input_check(email).check_email('Почта') == False:
            return

        # Password checks.
        if password == '':
            self.input_check().simple_diag(
                'Нельзя создать пустой пароль пользователя.')
            return
        elif self.input_check(password).check_incorrect_vals('Пароль') == False:
            return
        elif self.input_check(password).check_len('Пароль') == False:
            return
        elif self.input_check(password).check_spaces_tabs('Пароль') == False:
            return
        if len(password) <= 7:
            self.input_check().simple_diag(
                'Длина пароля должна быть не менее 8 символов.')
            return
        if self.rUi.register_checkbox_agree.isChecked() == False:
            self.input_check().simple_diag(
                'Пожалуйста, примите условия пользования.')
            return

        self.timedb.register_user(login, email, password)

        if self.timedb.user_input_check == '1':
            self.input_check().simple_diag(
                'Данный пользователь уже зарегистрирован.')
            return
        elif self.timedb.user_input_check == '2':
            self.input_check().simple_diag(
                'Данный email уже зарегистрирован.')
            return
        else:
            self.rUi.close()
            self.mUi.show()

    def update_users_categs(self):
        self.aUi.add_event_comboBox_category.clear()
        self.eUi.edit_event_comboBox_category.clear()

        categs, i = self.timedb.get_logged_user_data(
            item='get_user_categories'), 0
        for categ in categs:
            self.aUi.add_event_comboBox_category.insertItem(i, categ)
            self.eUi.edit_event_comboBox_category.insertItem(i, categ)
        i += 1

    # FOR TABLE AND EDIT_EVENT.

    def get_current_row_tableview(self, item):
        '''
        Current method displays clicked column and row of a choosen cell 
        in a TableView widget.
        '''
        # #selected cell value.
        self.act_id = str(item.sibling(item.row(), 0).data())
        self.act_date = str(item.sibling(item.row(), 1).data())
        self.cat_name = str(item.sibling(item.row(), 2).data())
        self.actl_name = str(item.sibling(item.row(), 3).data())
        self.act_time = str(item.sibling(item.row(), 4).data())
        self.act_comment = str(item.sibling(item.row(), 5).data())

        # self.act_id, self.actl_id = \
        #     self.timedb.get_logged_user_data(item='get_act_id',\
        #         params=[self.actl_name, self.act_time, self.act_date,\
        #             self.cat_name, self.act_comment]),\
        #         self.timedb.get_logged_user_data(item='get_actl_id',\
        #             params=[self.cat_name, self.actl_name])

        self.show_edit_action(self.actl_name, self.act_time, self.act_date,
                              self.cat_name, self.act_comment)
        # print(self.act_comment)
        # def show_edit_event(self, actl_name=str, act_time=str, act_date=None,
        #                 cat_name=str, act_comment=None)
        # return self.actl_name

    # EDIT ACTION BLOCK. uses ActionsUI class, method add_event().
    def show_add_action(self):
        self.aUi.add_event_dateEdit.setCalendarPopup(True)
        self.aUi.add_event_dateEdit.setDate(
            QtCore.QDate(QtCore.QDate.currentDate()))
        self.aUi.add_event_dateEdit.setMaximumDate(
            QtCore.QDate(QtCore.QDate.currentDate()))

        self.aUi.show()

    def add_action(self):
        # Getting all info, entered by user.
        title = self.aUi.add_event_lineEdit_name.text()
        category = self.aUi.add_event_comboBox_category.currentText()
        duration = self.aUi.add_event_lineEdit_time.text()
        date = self.aUi.add_event_dateEdit.date()
        comment = self.aUi.add_event_plaintextedit_comment.toPlainText()

        # Title checks.
        if title == '':
            self.input_check().simple_diag(
                'Пожалуйста, дайте название своему событию.')
            return
        elif self.input_check(title).check_incorrect_vals('Название') == False:
            return
        elif self.input_check(title).check_len('Название') == False:
            return

        # Category checks.
        if category == '':
            self.input_check().simple_diag(
                'Пожалуйста, укажите категорию для своего события.')
            return
        elif self.input_check(category).check_incorrect_vals(
                'Категория') == False:
            return
        elif self.input_check(category).check_len('Категория') == False:
            return

        # Duration checks.
        if duration == '':
            self.input_check().simple_diag(
                'Пожалуйста, укажите потраченное время на активность в минутах.')
            return
        elif self.input_check(duration).check_number_only('Длительность') == False:
            return

        # Comment checks.
        if self.input_check(comment).check_incorrect_vals('Комментарий') == False:
            return
        elif self.input_check(comment).check_len('Комментарий') == False:
            return

        date_ = datetime.date(date.year(), date.month(), date.day())
        str_date = date_.strftime('%Y-%m-%d')

        int_duration = int(''.join(filter(str.isdigit, duration)))

        # Writing all changes to db and closing 'Add Event' win.
        if not self.timedb.set_logged_user_data(item='check_event_data',
                                                add_params=[category, title, int_duration, str_date, comment]) == True:
            self.timedb.set_logged_user_data(item='add_event',
                                             add_params=[category, title, int_duration, str_date, comment])

        self.update_users_categs()
        self.update_custom_view_table_test()
        self.aUi.close()

    # EDIT ACTION BLOCK. uses ActionsUI class, method show_edit_event().
    def show_edit_action(self, actl_name=str, act_time=str, act_date=None,
                         cat_name=str, act_comment=None):

        # self.act_id = self.timedb.get_logged_user_data(item='get_act_id',\
        #     params=[cat_name, act_time, act_date, actl_name, act_comment])

        # self.actl_id = self.timedb.get_logged_user_data(item='get_actl_id',\
        #     params=[actl_name, cat_name])

        self.eUi.edit_event_dateEdit.setCalendarPopup(True)
        self.eUi.edit_event_dateEdit.setMaximumDate(
            QtCore.QDate(QtCore.QDate.currentDate()))

        date_ = datetime.datetime.strptime(act_date, '%Y-%m-%d')
        for d in [date_.timetuple()]:
            year = int(d[0])
            month = int(d[1])
            day = int(d[2])
            date = QtCore.QDate(year, month, day)

        self.eUi.edit_event_lineEdit_name.setText(actl_name)
        self.eUi.edit_event_comboBox_category.setCurrentText(cat_name)
        self.eUi.edit_event_lineEdit_time.setText(act_time)
        self.eUi.edit_event_dateEdit.setDate(date)
        self.eUi.edit_event_plaintextedit_comment.setPlainText(act_comment)

        self.eUi.show()

    def edit_action(self):
        title = self.eUi.edit_event_lineEdit_name.text()
        category = self.eUi.edit_event_comboBox_category.currentText()
        duration = self.eUi.edit_event_lineEdit_time.text()
        date = self.eUi.edit_event_dateEdit.date()
        comment = self.eUi.edit_event_plaintextedit_comment.toPlainText()

        chck_title = InputCheck(title)
        chck_category = InputCheck(category)
        chck_duration = InputCheck(duration)
        chck_comment = InputCheck(comment)

        # Title checks.
        if title == '':
            self.input_check().simple_diag(
                'Пожалуйста, дайте название своему событию.')
            return
        elif self.input_check(title).check_incorrect_vals('Название') == False:
            return
        elif self.input_check(title).check_len('Название') == False:
            return

        # Category checks.
        if category == '':
            self.input_check().simple_diag(
                'Пожалуйста, укажите категорию для своего события.')
            return
        elif self.input_check(category).check_incorrect_vals(
                'Категория') == False:
            return
        elif self.input_check(category).check_len('Категория') == False:
            return

        # Duration checks.
        if duration == '':
            self.input_check().simple_diag(
                'Пожалуйста, укажите потраченное время на активность в минутах.')
            return
        elif self.input_check(duration).check_number_only('Длительность') == False:
            return

        # Comment checks.
        if self.input_check(comment).check_incorrect_vals('Комментарий') == False:
            return
        elif self.input_check(comment).check_len('Комментарий') == False:
            return

        date_ = datetime.date(date.year(), date.month(), date.day())
        str_date = date_.strftime('%Y-%m-%d')

        int_duration = int(''.join(filter(str.isdigit, duration)))

        # Writing all changes to db and closing 'Add Event' win.
        self.timedb.set_logged_user_data(item='check_event_data',
                                         add_params=[self.cat_name, self.actl_name, self.act_time, self.act_date,
                                                     self.act_comment, self.act_id])
        self.timedb.set_logged_user_data(item='edit_event',
                                         add_params=[self.cat_name, self.actl_name, self.act_time, self.act_date,
                                                     self.act_comment, self.act_id],
                                         edit_params=[category, title, int_duration, str_date, comment])

        self.update_users_categs()
        self.update_custom_view_table_test()
        self.eUi.close()

    def delete_action(self):
        self.timedb.set_logged_user_data(item='del_event',
                                         add_params=[self.cat_name, self.actl_name, self.act_time, self.act_date,
                                                     self.act_comment, self.act_id])

        self.update_users_categs()
        self.update_custom_view_table_test()
        self.eUi.close()

    # SETTINGS BLOCK.
    def settings(self):
        # Shows settings win.
        self.sUi.show()

    def settings_export(self):
        data = self.timedb.get_logged_user_data(item='get_user_activities')
        try:
            settingsSave, ok = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file',
                                                                     '/', 'CSV file (*.csv)')
            if settingsSave[0]:
                with open(settingsSave[0], 'w+', newline='') as f:
                    writer = csv.writer(f)
                    for d in data:
                        writer.writerow(d)

        except Exception:
            self.input_check().simple_diag('Экспорт не удался.')
        if ok:
            self.input_check().simple_diag('Экспорт успешно завершён!')

    def settings_import(self):
        try:
            settingsLoad, ok = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file',
                                                                     '/', 'CSV file (*.csv)')
            if settingsLoad[0]:
                with open(settingsLoad[0], 'r+') as f:
                    reader = csv.reader(f, delimiter=',')
                    for row in reader:
                        if not self.timedb.set_logged_user_data(item='check_event_data',
                                                                add_params=row) == True:
                            self.timedb.set_logged_user_data(
                                item='add_event', add_params=row)

        except Exception:
            self.input_check().simple_diag('Импорт не удался.')
        if ok:
            self.input_check().simple_diag('Импорт успешно завершён!')

    def settings_change_user_data(self):
        self.timedb.get_logged_user_data(item='get_user_p_id')
        email_new = self.sUi.settings_lineedit_email_new.text()
        oldpass = self.sUi.settings_lineedit_oldpass.text()
        newpass = self.sUi.settings_lineedit_newpass.text()
        rep_newpass = self.sUi.settings_lineedit_repnewpass.text()

        if email_new == '' and oldpass == '' and newpass == '' and rep_newpass == '':
            self.input_check().simple_diag(
                f'Если Вы хотите изменить только текущую почту,\n'
                f'укажите новую почту и текущий пароль в соответсвующих полях.\n'
                f'Если Вы хотите изменить только текущий пароль,\n'
                f'укажите его в соостветсвующем поле, также заполнив поля ниже.\n'
                f'Для изменения всей информации, заполните все поля.')
            return

        # Change all data at once.
        if not email_new == '' and not oldpass == '' and not newpass == '' and not rep_newpass == '':
            if self.input_check(email_new).check_email('Новая почта') == False:
                return
            elif not oldpass == self.timedb.get_logged_user_data(
                    item='get_user_password'):
                self.input_check().simple_diag(
                    'Текущий пароль неверный.')
                return

            elif self.input_check(newpass).check_incorrect_vals(
                    'Новый пароль') == False:
                return
            elif self.input_check(newpass).check_len(
                    'Новый пароль') == False:
                return
            elif self.input_check(newpass).check_spaces_tabs(
                    'Новый пароль') == False:
                return
            elif self.input_check(newpass).check_password_len(
                    'Новый пароль') == False:
                return
            elif self.input_check(rep_newpass).check_incorrect_vals(
                    'Подтверждение пароля') == False:
                return
            elif self.input_check(rep_newpass).check_len(
                    'Подтверждение пароля') == False:
                return
            elif self.input_check(rep_newpass).check_spaces_tabs(
                    'Подтверждение пароля') == False:
                return
            elif self.input_check(rep_newpass).check_password_len(
                    'Подтверждение пароля') == False:
                return
            elif not newpass == rep_newpass:
                self.input_check().simple_diag(
                    'Новый пароль не совпадает с его повторением.')
                return
            else:
                self.timedb.set_logged_user_data(
                    item='change_email', edit_params=[email_new])
                self.timedb.set_logged_user_data(
                    item='change_password', edit_params=[newpass])
                self.input_check().simple_diag(
                    'Пароль и почта успешно изменены!')
                self.sUi.settings_lineedit_email.setText(
                    self.timedb.get_logged_user_data(item='get_user_email'))
                return

        # Change email checks.
        if not email_new == '' and oldpass == '' and newpass == '' and rep_newpass == '':
            self.input_check().simple_diag(
                'Введите старый пароль для изменения почты.')
            return
        elif not email_new == '' and not oldpass == '' and newpass == '' and rep_newpass == '':
            if self.input_check(email_new).check_email('Новая почта') == False:
                return
            elif not oldpass == self.timedb.get_logged_user_data(
                    item='get_user_password'):
                self.input_check().simple_diag(
                    'Текущий пароль неверный.')
                return
            else:
                self.timedb.set_logged_user_data(
                    item='change_email', edit_params=[email_new])
                self.input_check().simple_diag(
                    'Почта успешно изменена!')
                self.sUi.settings_lineedit_email.setText(
                    self.timedb.get_logged_user_data(item='get_user_email'))
                return

        # Change password checks.
        if not oldpass == '' and newpass == '' and rep_newpass == '':
            self.input_check().simple_diag(
                'Введите новый пароль или новую почту для изменений.')
            return
        elif not oldpass == '' and not newpass == '' and rep_newpass == '':
            self.input_check().simple_diag(
                'Подтвердите новый пароль для изменения старого.')
            return
        elif not oldpass == '' and not newpass == '' and not rep_newpass == '' and email_new == '':
            if not oldpass == self.timedb.get_logged_user_data(
                    item='get_user_password'):
                self.input_check().simple_diag(
                    'Текущий пароль неверный.')
                return
            elif self.input_check(newpass).check_incorrect_vals(
                    'Новый пароль') == False:
                return
            elif self.input_check(newpass).check_len(
                    'Новый пароль') == False:
                return
            elif self.input_check(newpass).check_spaces_tabs(
                    'Новый пароль') == False:
                return
            elif self.input_check(newpass).check_password_len(
                    'Новый пароль') == False:
                return
            elif self.input_check(rep_newpass).check_incorrect_vals(
                    'Подтверждение пароля') == False:
                return
            elif self.input_check(rep_newpass).check_len(
                    'Подтверждение пароля') == False:
                return
            elif self.input_check(rep_newpass).check_spaces_tabs(
                    'Подтверждение пароля') == False:
                return
            elif self.input_check(rep_newpass).check_password_len(
                    'Подтверждение пароля') == False:
                return
            elif not newpass == rep_newpass:
                self.input_check().simple_diag(
                    'Новый пароль не совпадает с его повторением.')
                return
            else:
                self.timedb.set_logged_user_data(
                    item='change_password', edit_params=[newpass])
                self.input_check().simple_diag(
                    'Пароль успешно изменён!')
                self.sUi.settings_lineedit_email.setText(
                    self.timedb.get_logged_user_data(item='get_user_email'))
                return

    def settings_telegram(self):
        if not self.timedb.get_logged_user_data(
            item='get_user_telegram') == '0' and not self.timedb.get_logged_user_data(
                item='get_user_telegram') == 'None':
            msg = self.input_check(
                buttons=['Отвязать телеграм', 'Открыть бота']).simple_diag(
                    'Пожалуйста, выберите действие:')
            if msg == 5:
                self.timedb.set_logged_user_data(item='del_telegram')
                self.input_check().simple_diag('Телеграм успешно отвязан!')
            elif msg == 6:
                webbrowser.open_new_tab(
                    'https://web.telegram.org/#/im?p=@fexcin_bot')
        else:
            webbrowser.open_new_tab(
                'https://web.telegram.org/#/im?p=@fexcin_bot')

    # TABLE VIEWING BLOCK. uses DbLogic class.
    def custom_view_table(self):
        rows = self.timedb.get_logged_user_data(item='get_user_activities')
        self.lay = QtWidgets.QHBoxLayout()
        self.tUi.tableW.setRowCount(len(rows))

        x = 0
        for row in rows:
            self.tUi.tableW.horizontalHeader().sortIndicatorOrder()
            self.tUi.tableW.setItem(x, 0,
                                    QtWidgets.QTableWidgetItem(row[3]))
            self.tUi.tableW.setItem(x, 1,
                                    QtWidgets.QTableWidgetItem(row[0]))
            self.tUi.tableW.setItem(x, 2,
                                    QtWidgets.QTableWidgetItem(row[1]))
            self.tUi.tableW.setItem(x, 3,
                                    QtWidgets.QTableWidgetItem(row[2]))
            self.tUi.tableW.setItem(x, 4,
                                    QtWidgets.QTableWidgetItem(row[4]))
            x += 1

        self.tUi.tableW.resizeColumnsToContents()
        self.tUi.tableW.verticalHeader().setVisible(False)
        self.tUi.tableW.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self.lay.addWidget(self.tUi.tableW)
        self.wUi.setLayout(self.lay)

    # TABLE VIEWING BLOCK. uses DbLogic class.
    def custom_view_table_test(self):
        rows = self.timedb.get_logged_user_data(
            item='get_user_activities_test')
        # self.lay = QtWidgets.QHBoxLayout()
        self.ttUi.tableW.setRowCount(len(rows))

        x = 0
        for row in rows:
            # self.ttUi.tableW.horizontalHeader().sortIndicatorOrder()
            self.ttUi.tableW.setItem(x, 0,
                                     QtWidgets.QTableWidgetItem(str(row[0])))
            self.ttUi.tableW.setItem(x, 1,
                                     QtWidgets.QTableWidgetItem(row[4]))
            self.ttUi.tableW.setItem(x, 2,
                                     QtWidgets.QTableWidgetItem(row[1]))
            self.ttUi.tableW.setItem(x, 3,
                                     QtWidgets.QTableWidgetItem(row[2]))
            self.ttUi.tableW.setItem(x, 4,
                                     QtWidgets.QTableWidgetItem(row[3]))
            self.ttUi.tableW.setItem(x, 5,
                                     QtWidgets.QTableWidgetItem(row[5]))
            x += 1

        self.ttUi.tableW.resizeColumnsToContents()
        self.ttUi.tableW.verticalHeader().setVisible(False)
        self.ttUi.tableW.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self.lay.addWidget(self.ttUi.tableW)
        # self.wUi.setLayout(self.lay)

    def update_custom_view_table(self):
        # self.lay.removeWidget(self.tUi)
        self.tUi.tableW.setParent(None)  # Removing tUi widget from wUi.

        rows = self.timedb.get_logged_user_data(item='get_user_activities')

        self.tUi.tableW.setRowCount(len(rows))

        x = 0
        for row in rows:
            # self.ttUi.tableW.horizontalHeader().sortIndicatorOrder()
            self.ttUi.tableW.setItem(x, 0,
                                     QtWidgets.QTableWidgetItem(row[0]))
            self.ttUi.tableW.setItem(x, 1,
                                     QtWidgets.QTableWidgetItem(row[4]))
            self.ttUi.tableW.setItem(x, 2,
                                     QtWidgets.QTableWidgetItem(row[1]))
            self.ttUi.tableW.setItem(x, 3,
                                     QtWidgets.QTableWidgetItem(row[2]))
            self.ttUi.tableW.setItem(x, 4,
                                     QtWidgets.QTableWidgetItem(row[3]))
            self.ttUi.tableW.setItem(x, 5,
                                     QtWidgets.QTableWidgetItem(row[5]))
            x += 1

        self.tUi.tableW.resizeColumnsToContents()
        self.tUi.tableW.verticalHeader().setVisible(False)
        self.tUi.tableW.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self.lay.addWidget(self.tUi.tableW)

    def update_custom_view_table_test(self):
        # self.lay.removeWidget(self.tUi)
        # self.tUi.tableW.setParent(None) # Removing tUi widget from wUi.
        for i in reversed(range(self.lay.count())):
            self.lay.itemAt(i).widget().setParent(None)

        rows = self.timedb.get_logged_user_data(
            item='get_user_activities_test')

        self.ttUi.tableW.setRowCount(len(rows))

        x = 0
        for row in rows:
            self.ttUi.tableW.horizontalHeader().sortIndicatorOrder()
            self.ttUi.tableW.setItem(x, 0,
                                     QtWidgets.QTableWidgetItem(str(row[0])))
            self.ttUi.tableW.setItem(x, 1,
                                     QtWidgets.QTableWidgetItem(row[4]))
            self.ttUi.tableW.setItem(x, 2,
                                     QtWidgets.QTableWidgetItem(row[1]))
            self.ttUi.tableW.setItem(x, 3,
                                     QtWidgets.QTableWidgetItem(row[2]))
            self.ttUi.tableW.setItem(x, 4,
                                     QtWidgets.QTableWidgetItem(row[3]))
            self.ttUi.tableW.setItem(x, 5,
                                     QtWidgets.QTableWidgetItem(row[5]))
            x += 1
            print(row)

        self.ttUi.tableW.resizeColumnsToContents()
        self.ttUi.tableW.verticalHeader().setVisible(False)
        self.ttUi.tableW.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self.lay.addWidget(self.ttUi.tableW)

    def graph_plot(self):
        # removing all widgets.
        # Removing tUi widget from wUi.

        rows = self.timedb.get_logged_user_data(item='get_user_activities')
        # Checking if combobox status is Graph.
        # Getting categories array(similar not repeated) and
        # sum of the corresponding durations array for them.
        self.categories = []  # array of all (repeatable) categories.
        self.duration = []  # array of all durations.
        self.diff_duration = []  # array of apropriate sum of durations
        # positioning relatively to the corresponding fields of non-repeatable
        # field of categories.
        self.num_diff_categories = []

        for row in rows:
            self.categories.append(row[0])
            self.duration.append(int(row[2]))

        self.diff_categories = list(
            (set([x for x in self.categories if self.categories.count(x) > 1])))

        for i in range(len(self.diff_categories)):
            self.diff_duration.append(0)

        self.item = 0
        self.diff_item = 0

        for i in self.categories:

            for j in self.diff_categories:
                if i == j:
                    self.diff_duration[self.diff_item] += self.duration[self.item]
                self.diff_item += 1

            self.item += 1
            self.diff_item = 0

        inc = 0
        for i in self.diff_categories:
            self.num_diff_categories.append(inc)
            inc += 1

        # Displaying the table if combobox current index is equal to 0.
        if self.mUi.mainwindow_comboBox_display_style.currentIndex() == 0:
            # Removing all widgets from layout.
            for i in reversed(range(self.lay.count())):
                self.lay.itemAt(i).widget().setParent(None)

            self.lay.addWidget(self.ttUi.tableW)

        # Displaying the diagram/chart if combobox current index is equal to 1.
        elif self.mUi.mainwindow_comboBox_display_style.currentIndex() == 1:
            # Removing all widgets from layout.
            for i in reversed(range(self.lay.count())):
                self.lay.itemAt(i).widget().setParent(None)

            series = QPieSeries()
            # Appending values to series.
            for i in range(len(self.diff_categories)):
                series.append(self.diff_categories[i], self.diff_duration[i])

            # adding slice
            slice = QPieSlice()
            slice = series.slices()[2]
            slice.setExploded(True)
            slice.setLabelVisible(True)
            slice.setPen(QPen(Qt.darkGreen, 2))
            slice.setBrush(Qt.green)

            chart = QChart()
            chart.legend().hide()
            chart.addSeries(series)
            chart.createDefaultAxes()
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chart.setTitle("Круговая диаграмма потраченого времени")

            # chart.setPlotAreaBackgroundBrush(QBrush(Qt.black))
            # chart.setPlotAreaBackgroundVisible(True)
            # chart.setBackgroundPen(QPen(Qt.darkGreen))
            # chart.setPlotAreaBackgroundPen(QPen(Qt.darkGreen))
            # chart.setPlotAreaBackgroundBrush(Qt.green)

            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignBottom)

            chartview = QChartView(chart)
            chartview.setRenderHint(QPainter.Antialiasing)

            self.lay.addWidget(chartview)

        # Displaying the graph if combobox current index is equal to 2.
        elif self.mUi.mainwindow_comboBox_display_style.currentIndex() == 2:
            # Removing all widgets from layout.
            for i in reversed(range(self.lay.count())):
                self.lay.itemAt(i).widget().setParent(None)

            # print(f'Categories: {self.diff_categories}')
            # print(f'Duration: {self.diff_duration}')
            # print(f'Number of categories: {self.num_diff_categories}')

            # combobox.currentIndexChanged().connect(updateGraph)

            ticks = [
                list(zip(range(len(self.diff_categories)), (self.diff_categories)))]

            # self.tUi.tableW.setParent(None) # Removing tUi widget from wUi.
            self.graphWidget = pg.PlotWidget()  # Plotting graphwidget.

            # Replacing x axis of our graph by customised words.
            xax = self.graphWidget.getAxis('bottom')
            xax.setTicks(ticks)

            # Adding graphwidget to layout.
            self.lay.addWidget(self.graphWidget)

            # cc = pg.colormap.get('CET-L17') # prepare a linear color map
            # cm.reverse() # reverse it to put light colors at the top
            pen = pg.mkPen(color=(115, 103, 240), width=2)
            # self.graphWidget.setConfigOption('background', (40, 48, 70))
            # pen = pg.mkPen(color=(255, 0, 0)) # Adding color to the graph curve.
            self.graphWidget.setTitle(
                "<span style=\"color:white;font-size:18pt\">График потраченого времени</span>")
            # styles = {'color':'r', 'font-size':'20px'}
            self.graphWidget.setBackground((40, 48, 70))
            self.graphWidget.setLabel(
                'left', "<span style=\"color:white;font-size:12px\">Время (мин.)</span>")
            self.graphWidget.setLabel(
                'bottom', "<span style=\"color:white;font-size:12px\">Активности (категории)</span>")
            self.graphWidget.plot(self.num_diff_categories,
                                  self.diff_duration, pen=pen)


# ----------------------------------------------------------END-----timeSoft.py

# ----------------------------------------------------------START----dblogic.py


class DbLogic:

    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8-sig')

    def __init__(self):
        self.connection = db.connect(database=self.config.get('PostgreSql', 'database'),
                                     user=self.config.get(
                                         'PostgreSql', 'user'),
                                     password=self.config.get(
                                         'PostgreSql', 'password'),
                                     host=self.config.get('PostgreSql', 'host'))

        self.cursor = self.connection.cursor()
        self.cursor2 = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)

        self.correct_login_info = False
        self.user_input_check = None

    # REGISTRATION AND AUTHORIZATION BLOCKS.
    def register_user(self, user_n_name, user_p_email, user_p_password):
        try:
            user_n_id = str(uuid4())
            user_p_id = str(uuid4())
            self.connection.autocommit = True

            self.cursor.execute(
                f'SELECT user_n_name = \'{user_n_name}\' FROM "USER_NAME"')
            lst = str(self.cursor.fetchall())
            if 'True' in lst:
                self.user_input_check = '1'
                return
            # Сделано в Китае. Разработано в России.
            self.cursor.execute(
                f'SELECT user_p_email = \'{user_p_email}\' FROM "USER_PRIVATE"')
            lst = str(self.cursor.fetchall())
            if 'True' in lst:
                self.user_input_check = '2'
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

            self.cursor.execute(
                f'SELECT user_n_id FROM "USER_NAME" WHERE user_n_name = \'{user_n_name}\'')
            user_n_id = str(self.cursor.fetchall())[3:-4]

            self.cursor.execute(
                f'SELECT user_p_id FROM "USER" WHERE user_n_id = \'{user_n_id}\'')
            user_p_id = str(self.cursor.fetchall())[3:-4]

            self.cursor.execute(
                f'SELECT user_p_email FROM "USER_PRIVATE" WHERE user_p_id = \'{user_p_id}\'')
            user_p_email = str(self.cursor.fetchall())[3:-4]

            self.cursor.execute(
                f'SELECT user_p_password FROM "USER_PRIVATE" WHERE\
                    user_p_id = \'{user_p_id}\' and user_p_email = \'{user_p_email}\'')
            user_password = str(self.cursor.fetchall())[3:-4]

            if not user_password == user_p_password:
                self.correct_login_info = False
            elif user_password == user_p_password:
                self.correct_login_info = True
        except Exception:
            pass

    def get_logged_user_data(self, user_login=None, item=None, params=None):
        # Setting working user in db.
        if item == 'set_working_user':
            self.cursor.execute(
                f'SELECT user_n_id FROM "USER_NAME" WHERE user_n_name = \'{user_login}\'')
            self.user_n_id = str(self.cursor.fetchall())[2:-3]

            self.cursor.execute(
                f'SELECT user_id FROM "USER" WHERE user_n_id = {self.user_n_id}')
            self.user_id = str(self.cursor.fetchall())[2:-3]
            return self.user_id

        # Getting actl_id.
        elif item == 'get_actl_id':
            self.cursor.execute(
                f'SELECT actl_id FROM "ACTIVITY_LIST" WHERE\
                (user_id, actl_name, cat_name) = (\'{self.user_id}\', \'{params[1]}\', \'{params[0]}\')')
            self.actl_id = str(self.cursor.fetchall())[2:-3]
            return self.actl_id

        # Getting act_id.
        elif item == 'get_act_id':
            self.cursor.execute(
                f'SELECT act_id FROM "ACTIVITY" WHERE\
                (user_id, actl_name, act_time, act_date, cat_name, act_comment) =\
                    (\'{self.user_id}\', \'{params[0]}\', \'{params[1]}\', \'{params[2]}\',\
                        \'{params[3]}\', \'{params[4]}\')')
            self.act_id = str(self.cursor.fetchall())[2:-3]
            return self.act_id

        # Getting user_p_id.
        elif item == 'get_user_p_id':
            self.cursor.execute(
                f'SELECT user_p_id FROM "USER" WHERE user_id = \'{self.user_id}\'')
            self.user_p_id = str(self.cursor.fetchall())[3:-4]
            return self.user_p_id

        # Getting user email.
        elif item == 'get_user_email':
            self.cursor.execute(
                f'SELECT user_p_email FROM "USER_PRIVATE" WHERE\
                    user_p_id = \'{self.user_p_id}\'')
            return str(self.cursor.fetchall())[3:-4]

        # Getting user password.
        elif item == 'get_user_password':
            self.cursor.execute(
                f'SELECT user_p_password FROM "USER_PRIVATE" WHERE\
                    user_p_id = \'{self.user_p_id}\'')
            return str(self.cursor.fetchall())[3:-4]

        # For getting user categories.
        elif item == 'get_user_categories':
            self.cursor2.execute(
                f'SELECT cat_name FROM "CATEGORY" WHERE user_id = \'{self.user_id}\'')
            self.user_categories = []
            for row in self.cursor2.fetchall():
                self.user_categories += row
            return self.user_categories

        # For getting all user activities.
        elif item == 'get_user_activities':
            self.cursor2.execute(
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

        elif item == 'get_user_activities_test':
            self.cursor2.execute(
                f'SELECT act_id, cat_name, actl_name, act_time, act_date, act_comment\
                    FROM "ACTIVITY" WHERE user_id = \'{self.user_id}\'')
            user_activities = []
            for row in self.cursor2.fetchall():
                # Setting date in str fromat.
                date_ = row[4].strftime('%Y-%m-%d')
                row[4] = date_
                # Setting duration in str fromat.
                duration = str(row[3])
                row[3] = duration
                # row[0] = str(row[0])
                # row[1] = str(row[1])
                # row[2] = str(row[2])
                # row[5] = str(row[0])
                user_activities.append(row)
            return user_activities

        elif item == 'get_user_telegram':
            self.cursor.execute(
                f'SELECT user_n_telegram FROM "USER_NAME" WHERE user_n_id = {self.user_n_id}')
            return str(self.cursor.fetchall())[3:-4]

    def set_logged_user_data(self, user_login=None, item=None, add_params=None, edit_params=None):
        # params[0] = cat_name
        # params[1] = actl_name
        # params[2] = act_time
        # params[3] = act_date
        # params[4] = act_comment

        # Setting working user in db.
        if item == 'set_working_user':
            self.user_id = self.get_logged_user_data(
                user_login=user_login, item='set_working_user')
            return self.user_id

        # Storing user_p_id
        self.user_p_id = self.get_logged_user_data(item='get_user_p_id')

        # Сhecking for an existing record in db.
        if item == 'check_event_data':
            # Storing actl_id, using get_logged_user_data().
            self.actl_id = self.get_logged_user_data(
                item='get_actl_id', params=[add_params[0], add_params[1]])

            # Storing act_id, using get_logged_user_data().
            self.act_id = self.get_logged_user_data(
                item='get_act_id', params=[add_params[1], add_params[2],
                                           add_params[3], add_params[0], add_params[4]])

            # Checking for matching same category in db.
            self.user_categories = self.get_logged_user_data(
                item='get_user_categories')
            for row in self.user_categories:
                if row == add_params[0]:
                    break
            else:  # If not matching, adding category to db.
                self.cursor2.execute(
                    f'INSERT INTO "CATEGORY" (user_id, cat_name) VALUES (%s,%s)',
                    (self.user_id, add_params[0]))

                self.connection.commit()

        # Adding event as itself.
        elif item == 'add_event':
            self.set_logged_user_data(item='check_user_categories')

            self.cursor2.execute(
                f'INSERT INTO "ACTIVITY_LIST" (user_id, actl_name, cat_name)\
                    VALUES (%s,%s,%s) ON CONFLICT DO NOTHING', (self.user_id,
                                                                add_params[1], add_params[0]))

            self.cursor2.execute('INSERT INTO "ACTIVITY" (user_id, actl_name,\
                        act_time, act_date, cat_name, act_comment)\
                            VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING',
                                 (self.user_id, add_params[1], add_params[2], add_params[3], add_params[0],
                                  add_params[4]))

            self.connection.commit()

        # Editing existing event in db.
        elif item == 'edit_event':
            self.set_logged_user_data(item='check_user_categories')

            self.cursor2.execute(
                f'UPDATE "ACTIVITY_LIST" SET (actl_name, cat_name) = (\'{edit_params[1]}\',\
                    \'{edit_params[0]}\') WHERE actl_id = \'{self.actl_id}\'')

            self.cursor2.execute(
                f'UPDATE "ACTIVITY" SET (actl_name, act_time, act_date, cat_name, \
                    act_comment) = (\'{edit_params[1]}\', \'{edit_params[2]}\', \'{edit_params[3]}\',\
                        \'{edit_params[0]}\', \'{edit_params[4]}\') WHERE act_id = \'{add_params[5]}\'')

            self.connection.commit()

        # Deleting existing event.
        elif item == 'del_event':
            self.cursor.execute(
                f'DELETE FROM "ACTIVITY_LIST" WHERE user_id = \'{self.user_id}\' and \
                    actl_name = \'{add_params[1]}\' and cat_name = \'{add_params[0]}\'')

            self.cursor.execute(
                f'DELETE FROM "ACTIVITY" WHERE act_id = \'{add_params[5]}\'\
                    user_id = \'{self.user_id}\' and \
                    actl_name = \'{add_params[1]}\' and act_time = \'{add_params[2]}\' \
                        and act_date = \'{add_params[3]}\' and cat_name = \
                            \'{add_params[0]}\' and act_comment = \'{add_params[4]}\'')

            self.connection.commit()

        # Changing old user password to new.
        elif item == 'change_password':
            self.cursor2.execute(
                f'UPDATE "USER_PRIVATE" SET user_p_password = \'{edit_params[0]}\'\
                    WHERE user_p_id = \'{self.user_p_id}\'')

            self.connection.commit()

        # Changing old user email to new.
        elif item == 'change_email':
            self.cursor2.execute(
                f'UPDATE "USER_PRIVATE" SET user_p_email = \'{edit_params[0]}\'\
                    WHERE user_p_id = \'{self.user_p_id}\'')

            self.connection.commit()

        # Deleting telegram reference.
        elif item == 'del_tegeram':
            self.cursor2.execute(
                f'UPDATE "USER_NAME" SET user_n_telegram = 0\
                    WHERE user_n_id = \'{self.user_n_id}\'')

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
        # The number of rows in current TableView widget.
        self.table_rows_num = 0

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

# ----------------------------------------------------------END----dblogic.py


if __name__ == '__main__':
    # app = QtWidgets.QApplication(sys.argv)
    # win = MainUI()
    # sys.exit(app.exec())

    # dbl = DbLogic()
    # print(dbl.get_logged_user_data(user_login='Sif', item='set_working_user'))

    # print(dbl.get_logged_user_data(item='get_user_categories'))
    # print(dbl.get_logged_user_data(item='get_act_id', params=['Кушал1', '60', '2021-05-26', 'Еда', '1']))
    # print(dbl.get_logged_user_data(item='get_actl_id', params=['12', 'Kofe 3']))
    # print(dbl.get_logged_user_data(item='get_user_activities'))
    # print(dbl.get_logged_user_data(item='get_user_activities_test'))
    # print(dbl.get_logged_user_data(item='get_user_p_id'))
    # print(dbl.get_logged_user_data(item='get_user_email'))
    # print(dbl.get_logged_user_data(item='get_user_password'))
    # print(dbl.get_logged_user_data(item='get_user_telegram'))

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

    # app = QtWidgets.QApplication(sys.argv)
    # win = InputCheckWithDiags('tl@ea..a').check_email('Почта')
    # sys.exit(app.exec())
    # a = InputCheck
    # print(a(',').check_incorrect_vals())
