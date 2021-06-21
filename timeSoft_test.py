import sys
import string
import configparser
import csv
import webbrowser

from uuid import uuid4
from datetime import datetime, date

import psycopg2 as db
import psycopg2.extras
import pyqtgraph as pg
import pandas as pd
import statsmodels.formula.api as smf

from pandas import read_csv
from matplotlib import pyplot as plt

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QIcon, QPainter, QPen
from PyQt5.QtCore import QDate, Qt


sys.path.append(".")

"""
TODO
!Перед импортом задать вопрос - перезаписать или добавить?
!Автокомплит в добавлении\редактировании активностей.
!докстринги + комменты + пепы(до вторника).
! Не работает проверка на вводимые символы allowed_chars.

Отдельная функция для сортировки.
Сортировка по категориям выше приоритетом
Кнопки сверху должны делить дату.
сделать комбобокс для названия кативностей + авктокомлит после введения для категории
"""


class InputCheck:
    """
    The InputCheck class implements base checking system for various input data.
    Attributes:
        input_text (str):The string which can be checked using various methods.
    """

    def __init__(self, input_text):
        self.text = input_text

        # Поддержка русского и украинских алфавитов.
        allowed_letters = [1025, 1028, 1030, 1031, 1040, 1041, 1042, 1043,
                           1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051,
                           1052, 1053, 1054, 1055, 1056, 1057, 1058, 1059,
                           1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067,
                           1068, 1069, 1070, 1071, 1072, 1073, 1074, 1075,
                           1076, 1077, 1078, 1079, 1080, 1081, 1082, 1083,
                           1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091,
                           1092, 1093, 1094, 1095, 1096, 1097, 1098, 1099,
                           1100, 1101, 1102, 1103, 1105, 1108, 1110, 1111,
                           1168, 1169]

        allowed_chars = [32, 33, 35, 36, 37, 38, 40, 41, 42, 43, 45, 46, 58, 60,
                         61, 62, 63, 64, 94, 95, 161, 162, 163, 164, 165, 166,
                         167, 168, 169, 171, 174, 175, 176, 177, 178, 179, 181,
                         182, 183, 187, 188, 189, 190, 215, 247, 3647, 8352,
                         8353, 8354, 8355, 8356, 8357, 8358, 8359, 8360, 8361,
                         8362, 8363, 8364, 8365, 8366, 8367, 8368, 8369, 8370,
                         8371, 8372, 8373, 8374, 8375, 8376, 8377, 8378, 8379,
                         8380, 8381, 8382, 8383, 8528, 8529, 8530, 8531, 8532,
                         8533, 8534, 8535, 8536, 8537, 8538, 8539, 8540, 8541,
                         8542, 8543, 8544, 8545, 8546, 8547, 8548, 8549, 8550,
                         8551, 8552, 8553, 8554, 8555, 8556, 8557, 8558, 8559,
                         8560, 8561, 8562, 8563, 8564, 8565, 8566, 8567, 8568,
                         8569, 8570, 8571, 8572, 8573, 8574, 8575, 8592, 8593,
                         8594, 8595, 8709, 8710, 8711, 8712, 8713, 8714, 8715,
                         8716, 8717, 8718, 8719, 8720, 8721, 8722, 8723, 8724,
                         8725, 8726, 8727, 8728, 8729, 8730, 8731, 8732, 8733,
                         8734, 8735, 8736, 8737, 8738, 8739, 8740, 8741, 8742,
                         8743, 8744, 8745, 8746, 8747, 8748, 8749, 8750, 8751,
                         8752, 8753, 8754, 8755, 8756, 8757, 8758, 8759, 8760,
                         8761, 8762, 8763, 8764, 8765, 8766, 8767, 8768, 8769,
                         8770, 8771, 8772, 8773, 8774, 8775, 8776, 8777, 8778,
                         8779, 8780, 8781, 8782, 8783, 8784, 8785, 8786, 8787,
                         8788, 8789, 8790, 8791, 8792, 8793, 8794, 8795, 8796,
                         8797, 8798, 8799, 8800, 8801, 8802, 8803, 8804, 8805,
                         8806, 8807, 8808, 8809, 8810, 8811, 8812, 8813, 8814,
                         8815, 8816, 8817, 8818, 8819, 8820, 8821, 8822, 8823,
                         8824, 8825, 8826, 8827, 8828, 8829, 8830, 8831, 8832,
                         8833, 8834, 8835, 8836, 8837, 8838, 8839, 8840, 8841,
                         8842, 8843, 8844, 8845, 8846, 8847, 8848, 8849, 8850,
                         8851, 8852, 8853, 8854, 8855, 8856, 8857, 8858, 8859,
                         8860, 8861, 8862, 8863, 8864, 8865]

        # Russian and ukrainian symbols.
        self.correct_rus_vals = [chr(i) for i in allowed_letters]
        # All allowed characters.
        self.allowed_characters = [chr(i) for i in allowed_chars]

        # List contains codes of correct symbols.
        self.correct_vals = list(string.ascii_lowercase) + \
            list(string.ascii_uppercase)
        self.correct_vals_with_num = self.correct_vals + \
            [str(x) for x in range(0, 10)]

        # all allowed symbols (gluing the previous four).
        self.all = []
        self.all.extend(self.correct_rus_vals)
        self.all.extend(self.allowed_characters)
        self.all.extend(self.correct_vals)
        self.all.extend(self.correct_vals_with_num)

        self.incorrect_vals = ['"', '\'', '\\', ',', '--', ';',
                               '[', ']', '{', '}', '|']

    def check_email(self):
        """
        This method makes various checks for correct email.
        If the email passes verification, it returns True(bool) only.
        If not passes, it returns list that contains two values:
        False(bool) and error message(str).
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
        self.correct_vals.extend(['-', '_'])
        for k in includedomain:
            # Checking if there are empty substrings in the domain.
            if k == '':
                return [False, 'Доменное имя содержит пустую строку между точками.']
            # Checking if there are any illegal characters in substrings
            # of the domain.
            for n in k:
                if n not in self.correct_vals:
                    return [False, f'Недопустимый символ {n}']
            if (k[0] == '-') or (k[len(k)-1] == '-'):
                return [False, 'Доменное имя не может начинаться/заканчиваться знаком "-".']
        if len(name) > 60:
            return [False, 'Имя почты длиннее 60 символов.']

        # Add to the list of valid characters (; " ! : ,).
        self.correct_vals_with_num.extend(['.', ';', '"'])
        # Variables to track period and opening quotes.
        doubledot = False
        for k in name:
            if k not in self.correct_vals_with_num:
                return [False, f'Недопустимый символ. "{k}"']
            # Checking for two points in a row.
            if k == '.':
                if doubledot:
                    return [False, 'Две точки в названии почты.']
                else:
                    doubledot = True
        return True

    def check_date(self, mode='date'):
        # Checking date and its format.
        if mode == 'datetime' and self.text.isdigit():
            if int(self.text) == 0:
                return [False, 'Введено некорректное количество дней.']
            elif int(self.text) > (datetime.now() - datetime(year=1900, month=1, day=1)).days - 1:
                return [False, 'Введено количество дней, указывающее на дату ранее 1900 года.']
        elif len(self.text.split(', ')) in range(1, 3):
            for x in self.text.split(', '):
                try:
                    if datetime.strptime(x, '%d.%m.%Y') > datetime.now():
                        return [False, 'Дата должна не может быть больше сегодняшней ({0}).'.format(
                            datetime.now().strftime('%d.%m.%Y'))]
                except (ValueError, Exception):
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
        if not (0 < int(self.text) <= 1440):
            return [False, 'Введено ошибочное количество потраченных минут.']
        return True

    def check_incorrect_vals(self):
        vals = []
        for i in self.text:
            if i in self.incorrect_vals:
                vals.append(i)
        if vals:
            if len(vals) == 1:
                vals = f"Недопустимый символ ({str(vals)})"
            else:
                vals = f"Недопустимый символы ({', '.join(vals)})"
            return [False, vals]
        return True

    def check_spaces_tabs(self):
        n = len(self.text)
        if self.text in [' ' * n, '\t' * n, '\n' * n]:
            return [False, 'Пробел, табуляция или перенос строки.']
        return True

    def number_only(self):
        self.correct_vals.extend(['.', ';', '"'])
        self.correct_vals.extend(self.correct_rus_vals)
        for i in self.text:
            if i in self.correct_vals or i in self.incorrect_vals:
                return [False, 'Разрешено вводить только количество минут.']
        return True


class InputCheckWithDiags(QtWidgets.QMessageBox):
    """
    The InputCheckWithDiags displays error messages using InputCheck class.

    Attributes:
        input_text (str): Storing text to be checked.
    """

    def __init__(self, input_text=None):
        super().__init__()
        self.input_text = input_text
        self.setIcon(QtWidgets.QMessageBox.Information)
        self.setWindowIcon(QIcon('design\\img\\main\\favicon.png'))
        self.setWindowTitle('Ошибка!')

    def simple_diag(self, err_txt):
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.setWindowTitle('Внимание!')
        self.setText(err_txt)
        self.exec()

    def extended_diag(self, err_txt, buttons):
        self.setIcon(QtWidgets.QMessageBox.Question)
        self.setWindowTitle('TimeSoft')
        self.setText(err_txt)

        yes = self.addButton(buttons[0], self.AcceptRole)
        no = self.addButton(buttons[1], self.DestructiveRole)

        self.exec()

        if self.clickedButton() is yes:
            return True
        elif self.clickedButton() is no:
            return False

    def check_password_len(self, err_txt):
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)
        if len(self.input_text) < 8:
            self.setText(
                f'{err_txt}: Пароль должен состоять минимум из 8 символов.')
            self.exec()
            return False
        return True

    def check_email(self, err_txt):
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)
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
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)
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
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)
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
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)
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
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)
        try:
            chck_number_only = InputCheck(self.input_text).number_only()
            if chck_number_only[0] == False:
                self.setText(f'{err_txt}: {chck_number_only[1]}')
                self.exec()
                return False
        except Exception:
            pass
        return True

    def check_time_val(self, err_txt):
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)
        try:
            chck_time_val = InputCheck(self.input_text).check_time_value()
            if chck_time_val[0] == False:
                self.setText(f'{err_txt}: {chck_time_val[1]}')
                self.exec()
                return False
        except Exception:
            pass
        return True

    def secondsToText(self, secs, inp_type=None):
        days = secs//86400
        hours = (secs - days*86400)//3600
        minutes = (secs - days*86400 - hours*3600)//60
        if inp_type == 'categs':
            result = ("{} д. ".format(days) if days else "") + \
                ("{} ч. ".format(hours) if hours else "") + \
                ("{} м. ".format(minutes) if minutes else "")
            return result
        elif inp_type == None:
            result = ("{} д. ".format(days) if days else "") + \
                ("{} ч. ".format(hours) if hours else "") + \
                ("{} мин. ".format(minutes) if minutes else "")
            return result


class MainUI(QtWidgets.QMainWindow):
    """
    The MainUI class contains the following functional:
    - UI processing
    - Data forecasting
    - Comparison of the entered information with data from db.
    - User registration and login
    - Events handling (adding, editing, deleting)
    - User settings
    - Theme changing
    - Plotting graphs, diagrams and table
    - Sorting data in the table (by time: day, week, month, etc)
    - Logout
    """

    def __init__(self):
        super().__init__()
        # Creating DataBase instance.
        self.timedb = DbLogic()

        # Creating StyleShhets instance.
        self.theme = StyleSheets()

        # Loading UI interfaces.
        self.mUi = self.theme.mUi  # Main window ui.
        self.aUi = self.theme.aUi  # Add actions ui.
        self.eUi = self.theme.eUi  # Edit actions ui.
        self.cUi = self.theme.cUi  # Category del ui.
        self.rUi = self.theme.rUi  # Registration window ui.
        self.lUi = self.theme.lUi  # Login window ui.
        self.sUi = self.theme.sUi  # Settings window ui.
        self.ttUi = self.theme.ttUi  # Table ui.
        self.abUi = self.theme.abUi  # About us ui.

        # Creating list for future customizing various ui elements.
        self.big_uis = [
            self.mUi, self.rUi, self.lUi, self.sUi, self.ttUi, self.abUi]

        self.small_uis = [self.aUi, self.eUi, self.cUi]

        # Widget for viewing various data.
        self.wUi = self.theme.wUi

        # Widget for viewing user categories.
        self.ccUi = self.theme.ccUi
        self.scroll_ccUi = self.theme.scroll_ccUi

        # Current date in different formats (datetime and QDate)
        self.today = datetime.now()
        self.qtoday = QtCore.QDate.currentDate()

        # Various settings for different UI elements, such as connecting
        # buttons to slots and setting menubars.
        self.pre_initUI()

        # Connect TableView with mouseClick.
        self.ttUi.tableW.doubleClicked.connect(self.get_current_row_tableview)

        # self.ttUi.tableW.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # When starting a program, first login UI appears.
        self.show_login()

    def pre_initUI(self):
        self.theme.dark_theme()

        icon = QtGui.QIcon('design\\img\\main\\favicon.png')

        for row in self.big_uis:
            row.setFixedHeight(768)
            row.setFixedWidth(1280)
            row.setWindowIcon(icon)

        for row in self.small_uis:
            row.setFixedHeight(640)
            row.setFixedWidth(360)
            row.setWindowIcon(icon)

        # Connecting buttons to slots.
        # Main UI.
        self.mUi.mainwindow_btn_nav_add_act.clicked.connect(
            self.show_add_action)
        self.mUi.mainwindow_btn_settings.clicked.connect(self.sUi.show)
        self.mUi.mainwindow_btn_exit.clicked.connect(self.mUi.close)
        self.mUi.mainwindow_btn_theme.clicked.connect(self.change_theme)

        # Sorting by date buttons and dateEdit element.
        self.mUi.mainwindow_dateEdit_s.setDate(self.qtoday.addDays(-7))
        self.mUi.mainwindow_dateEdit_po.setDate(self.qtoday)

        self.mUi.mainwindow_dateEdit_s.dateChanged.connect(self.update_date)
        self.mUi.mainwindow_dateEdit_po.dateChanged.connect(self.update_date)

        self.mUi.mainwindow_btn_daily.clicked.connect(
            self.view_table_sort_by_day)
        self.mUi.mainwindow_btn_weekly.clicked.connect(
            self.view_table_sort_by_week)
        self.mUi.mainwindow_btn_monthly.clicked.connect(
            self.view_table_sort_by_month)
        self.mUi.mainwindow_btn_annually.clicked.connect(
            self.view_table_sort_by_year)
        self.mUi.mainwindow_dateEdit_s.dateChanged.connect(
            self.view_table_custom_sort)
        self.mUi.mainwindow_dateEdit_po.dateChanged.connect(
            self.view_table_custom_sort)
        self.mUi.mainwindow_btn_all.clicked.connect(
            self.view_table_clear_filter)
        # Combobox.
        self.mUi.mainwindow_comboBox_display_style.currentIndexChanged.connect(
            self.graph_plot)
        # Menubar Main UI.
        self.mUi.mainwindow_act_make_prediction.triggered.connect(
            self.forecast)
        self.mUi.mainwindow_act_settings.triggered.connect(self.sUi.show)
        self.mUi.mainwindow_act_exit.triggered.connect(self.mUi.close)

        self.mUi.mainwindow_act_add_event.triggered.connect(
            self.show_add_action)

        self.mUi.mainwindow_act_about_program.triggered.connect(self.abUi.show)

        # Theme of main window.
        self.mUi.mainwindow_act_light.triggered.connect(self.theme.white_theme)
        self.mUi.mainwindow_act_dark.triggered.connect(self.theme.dark_theme)

        # Help window.
        self.mUi.mainwindow_act_help.triggered.connect(self.help)

        # Login UI.
        self.lUi.login_btn_login.clicked.connect(self.login)
        self.lUi.login_btn_create_account.clicked.connect(
            self.show_registration)
        self.lUi.login_btn_theme.clicked.connect(self.change_theme)

        # Register UI.
        self.rUi.register_btn_login.clicked.connect(self.registration)
        self.rUi.register_btn_create.clicked.connect(self.show_login)
        self.rUi.register_btn_theme.clicked.connect(self.change_theme)

        # Add event UI.
        self.aUi.add_event_btn_add.clicked.connect(self.add_action)
        self.aUi.add_event_btn_cancel.clicked.connect(self.aUi.close)
        self.aUi.add_event_btn_exit.clicked.connect(self.aUi.close)

        # Edit event UI.
        self.eUi.edit_event_btn_save.clicked.connect(self.edit_action)
        self.eUi.edit_event_btn_del.clicked.connect(self.delete_action)
        self.eUi.edit_event_btn_exit.clicked.connect(self.eUi.close)

        # Category deleting UI.
        self.cUi.category_delete_btn_exit.clicked.connect(self.cUi.close)
        self.cUi.category_delete_btn_cancel.clicked.connect(self.cUi.close)
        self.cUi.category_delete_btn_delete.clicked.connect(self.del_categ)

        # Settings UI.
        self.sUi.settings_btn_export.clicked.connect(self.settings_export)
        self.sUi.settings_btn_import.clicked.connect(self.settings_import)
        self.sUi.settings_btn_apply.clicked.connect(
            self.settings_change_user_data)
        self.sUi.settings_btn_undo.clicked.connect(self.sUi.close)
        self.sUi.settings_btn_telegram.clicked.connect(self.settings_telegram)

        # About us UI.
        self.abUi.about_us_btn_exit.clicked.connect(self.abUi.close)

        # Table widget UI.
        self.ttUi.tableW.setColumnHidden(0, True)
        self.ttUi.tableW.setColumnHidden(5, True)
        self.ttUi.tableW.verticalHeader().setVisible(False)
        self.ttUi.tableW.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        # Forecast.
        self.mUi.mainwindow_btn_forecast.clicked.connect(self.forecast)

        # Layout creation and appending widget for viewing various data to it.
        self.lay = QtWidgets.QHBoxLayout()
        self.wUi.setLayout(self.lay)

        # Scroll area settings.
        self.scroll_ccUi.setFrameShape(self.scroll_ccUi.NoFrame)

        # TableW settings.
        self.ttUi.tableW.setFrameStyle(self.ttUi.tableW.NoFrame)

        # Variable of correctness login status.
        self.correct_login = False

        self.input_check = InputCheckWithDiags

    def sorting_data_csv(self):
        # This method sorting data by month and category.
        if self.idx < len(self.diff_categories):
            # Creating new files.
            with open(
                    f'./csv_data/{self.user_n_name}_{self.diff_categories[self.idx]}_data.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Month', 'Duration'])
                for item in self.duration_by_dates_and_categories:
                    if item['category'] == self.diff_categories[self.idx]:
                        writer.writerow([item['date'], item['duration']])
            self.idx += 1
            self.sorting_data_csv()
        else:
            pass

    def post_initUI(self):
        self.user_id = self.timedb.get_logged_user_data(
            user_login=self.user_n_name, item='set_working_user')
        self.timedb.get_logged_user_data(item='get_user_p_id')
        self.sUi.settings_lineedit_email.setText(
            self.timedb.get_logged_user_data(item='get_user_email'))
        if not self.timedb.get_logged_user_data(
                item='get_user_telegram') == 'None':
            self.sUi.settings_imglbl_telegram_noverify.setHidden(True)

        self.update_users_categs()

    def change_theme(self):
        if self.theme.status == True:
            self.theme.white_theme()
            self.theme.status = False
        elif self.theme.status == False:
            self.theme.dark_theme()
            self.theme.status = True

    def update_date(self):
        self.mUi.mainwindow_dateEdit_s.setMaximumDate(
            QDate(self.mUi.mainwindow_dateEdit_po.date()))

        self.mUi.mainwindow_dateEdit_po.setMinimumDate(
            QDate(self.mUi.mainwindow_dateEdit_s.date()))

        self.mUi.mainwindow_dateEdit_po.setMaximumDate(self.qtoday)

    def create_forecast_data(self):
        # This method creates data which can then be forcasted.
        self.graph_plot()
        rows = self.timedb.get_logged_user_data(item='get_user_activities')
        self.dates = []

        for row in rows:
            self.dates.append(row[3][0:-3])
        self.diff_dates = list(
            (set([x for x in self.dates if self.dates.count(x) > 1])))

        self.sorted_diff_dates = sorted(
            self.diff_dates, key=lambda x: datetime.strptime(x, '%Y-%m'))

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
                self.sum_of_durations = 0

    def forecast(self):
        # This method create forcasted values and plots graphical representaion.
        self.idx = 0  # Setting index for sorting data to 0.
        self.sorting_data_csv()

        # Applying forecasting.
        self.idx = 0
        while self.idx < len(self.diff_categories):
            with open(f'./csv_data/{self.user_n_name}_{self.diff_categories[self.idx]}_data.csv', 'r') as file:
                d = file.readlines()
                lastRow = d[-1][:7]
                year = lastRow[:4]
                month = lastRow[5:7]
                if month == '12':
                    year = str(int(year)+1)
                    month = '01'
                elif month == '10' or month == '11':
                    month = str(int(month)+1)
                else:
                    month = f'0{str(int(month)+1)}'

            data = pd.read_csv(
                f'./csv_data/{self.user_n_name}_{self.diff_categories[self.idx]}_data.csv')
            with open(
                    f'./csv_data/{self.user_n_name}_{self.diff_categories[self.idx]}_data.csv', 'a') as file:
                # get last month in csv file.
                data['x'] = data.index
                lm = smf.ols(formula='Duration ~ x', data=data).fit()
                y = pd.DataFrame(dict(x=[len(data)]))
                writer = csv.writer(file)
                writer.writerow(
                    [f'{year}-{month}', round(lm.predict(y.x).get(0))])
            self.idx += 1

        # Reading csv files and plotting graphs according to them.
        index = 0
        pathes = []
        plt.figure(figsize=(13, 7))

        for i in range(len(self.diff_categories)):
            data = pd.read_csv(
                f'./csv_data/{self.user_n_name}_{self.diff_categories[i]}_data.csv')
            path = f'./csv_data/{self.user_n_name}_{self.diff_categories[index]}_data.csv'
            pathes.append(path)
            # plot the time series.

            df = read_csv(pathes[i])
            df = pd.DataFrame(data, columns=['Month', 'Duration'])

            plt.plot(df['Month'], df['Duration'])

            plt.legend(self.diff_categories)

            index += 1
        plt.show()

    def show_login(self):
        """
        Current method shows user interface login window.
        """
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
            self.view_table()  # Viewing table.
            self.view_categ()
            self.lUi.close()
            self.mUi.show()
            self.correct_login = True
            self.create_forecast_data()  # Forecast data creation

    def show_registration(self):
        """
        Current method shows user interface registration window.
        """
        self.lUi.close()
        self.rUi.show()

    def registration(self):
        login = self.rUi.register_lineEdit_name.text()
        email = self.rUi.register_lineEdit_email.text()
        password = self.rUi.register_lineEdit_password.text()

        timo = DbLogic()
        timo.get_logged_user_data(user_login='Timo', item='set_working_user')

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
            self.user_n_name = login
            self.post_initUI()

            base_categs = timo.get_logged_user_data(
                item='get_user_activity_list')
            for row in base_categs:
                self.timedb.set_logged_user_data(
                    item='set_default_categs_and_activities', add_params=[row[1], row[0]])
            self.update_users_categs()
            self.view_table()  # Viewing table.
            self.view_categ()
            self.rUi.close()
            self.mUi.show()
            self.correct_login = True
            self.create_forecast_data()  # Forcast data creation

    def update_users_categs(self):
        self.aUi.add_event_comboBox_category.clear()
        self.eUi.edit_event_comboBox_category.clear()
        self.cUi.category_delete_comboBox_category.clear()

        categs, i = self.timedb.get_logged_user_data(
            item='get_user_categories'), 0
        for categ in categs:
            self.aUi.add_event_comboBox_category.insertItem(i, categ)
            self.eUi.edit_event_comboBox_category.insertItem(i, categ)
            self.cUi.category_delete_comboBox_category.insertItem(i, categ)
            i += 1

    def get_current_row_tableview(self, item):
        """
        Current method displays clicked column and row of a choosen cell
        in a TableView widget.
        """
        # selected cell value.
        self.act_id = str(item.sibling(item.row(), 0).data())
        self.act_date = str(item.sibling(item.row(), 1).data())
        self.cat_name = str(item.sibling(item.row(), 2).data())
        self.actl_name = str(item.sibling(item.row(), 3).data())
        self.act_time = str(self.timedb.set_logged_user_data(
            item='get_act_time', add_params=[self.act_id]))
        self.act_comment = str(item.sibling(item.row(), 5).data())

        if self.actl_name[-1] == '*':
            self.actl_name = self.actl_name.removesuffix('*')

        self.show_edit_action(
            self.actl_name, self.act_time, self.act_date, self.cat_name, self.act_comment)

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
        date_ = self.aUi.add_event_dateEdit.date()
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
        # Duration checks.
        if duration == '':
            self.input_check().simple_diag(
                'Пожалуйста, укажите потраченное время на активность в минутах.')
            return
        elif self.input_check(duration).check_number_only(
                'Длительность') == False:
            return
        elif self.input_check(duration).check_time_val(
                'Длительность') == False:
            return

        # Comment checks.
        if self.input_check(comment).check_incorrect_vals('Комментарий') == False:
            return
        elif len(comment) > 500:
            self.input_check().simple_diag(
                'Длительность комментария превышает 500 символов.')
            return

        _date = date(date_.year(), date_.month(), date_.day())
        str_date = _date.strftime('%Y-%m-%d')

        int_duration = int(''.join(filter(str.isdigit, duration)))

        # Writing all changes to db and closing 'Add Event' win.
        self.timedb.set_logged_user_data(
            item='add_event', add_params=[
                category, title, int_duration, str_date, comment])

        self.update_users_categs()
        self.update_view_table()
        self.update_view_categ()
        self.aUi.close()

    def show_edit_action(self, actl_name=str, act_time=str, act_date=None,
                         cat_name=str, act_comment=None):

        self.eUi.edit_event_dateEdit.setCalendarPopup(True)
        self.eUi.edit_event_dateEdit.setMaximumDate(
            QtCore.QDate(QtCore.QDate.currentDate()))

        date_ = datetime.strptime(act_date, '%Y-%m-%d')
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
        date_ = self.eUi.edit_event_dateEdit.date()
        comment = self.eUi.edit_event_plaintextedit_comment.toPlainText()

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
        elif self.input_check(duration).check_number_only(
                'Длительность') == False:
            return
        elif self.input_check(duration).check_time_val(
                'Длительность') == False:
            return

        # Comment checks.
        if self.input_check(comment).check_incorrect_vals('Комментарий') == False:
            return
        elif len(comment) > 500:
            self.input_check().simple_diag(
                'Длительность комментария превышает 500 символов.')
            return

        _date = date(date_.year(), date_.month(), date_.day())
        str_date = _date.strftime('%Y-%m-%d')

        int_duration = int(''.join(filter(str.isdigit, duration)))

        # Writing all changes to db and closing 'Add Event' win.
        self.timedb.set_logged_user_data(
            item='edit_event', add_params=[
                self.cat_name, self.actl_name, self.act_time, self.act_date,
                self.act_comment, self.act_id], edit_params=[
                category, title, int_duration, str_date, comment])

        self.update_users_categs()
        self.update_view_table()
        self.update_view_categ()
        self.eUi.close()

    def delete_action(self):
        self.timedb.set_logged_user_data(
            item='del_event', add_params=[
                self.cat_name, self.actl_name, self.act_id])
        self.update_users_categs()
        self.update_view_table()
        self.update_view_categ()
        self.eUi.close()

    def del_categ(self):
        category = self.cUi.category_delete_comboBox_category.currentText()

        msg = self.input_check().extended_diag(
            f'При удалении категории, все связанные с ней данные,\n'
            f'включая Ваши добавленные активности, будут удалены. Продолжить?',
            ['Да', 'Нет'])

        if msg == True:
            self.timedb.set_logged_user_data(
                item='del_user_categ', add_params=[category])
        elif msg == False:
            self.cUi.close()

        self.update_users_categs()
        self.update_view_table()
        self.update_view_categ()
        self.cUi.close()

    # TODO:
    def settings_export(self):
        data = self.timedb.get_logged_user_data(item='get_user_activities')
        try:
            settingsSave, ok = QtWidgets.QFileDialog.getSaveFileName(
                self, 'Save file', '/', 'CSV file (*.csv)')
            if settingsSave:
                with open(settingsSave, 'w+', newline='') as f:
                    writer = csv.writer(f)
                    for d in data:
                        writer.writerow(d)
                if ok:
                    self.input_check().simple_diag('Экспорт успешно завершён!')
        except Exception:
            self.input_check().simple_diag('Экспорт не удался.')

    #!
    def settings_import(self):
        # progress = QtWidgets.QProgressDialog(
        #     'Производится импорт активностей без перезаписи...',\
        #         'Отмена', 0, 100, self)
        # progress.setWindowModality(Qt.WindowModal)
        try:
            settingsLoad, ok = QtWidgets.QFileDialog.getOpenFileName(
                self, 'Open file', '/', 'CSV file (*.csv)')
            if settingsLoad[0]:
                with open(settingsLoad[0], 'r+') as f:
                    reader = csv.reader(f, delimiter=',')
                    import_rows = []
                    for row in reader:
                        import_rows.append((row))

                # progress.show()
                # progress.setValue(0)
                # for i in range(101):
                #     progress.setValue(self.timedb.current_import_status)
                # for i in self.timedb.current_import_status:
                #     progress.setValue(i)
                # for i in range(101):
                #     print(i)
                    # self.timedb.set_logged_user_data(
                    #     item='import_add', edit_params=import_rows)
            # if ok:
            #     self.input_check().simple_diag('Импорт успешно завершён!')
        except Exception as e:
            self.input_check().simple_diag('Импорт не удался.')
            print(e)

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
                'Введите текущий пароль для изменения почты.')
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
                item='get_user_telegram') == 'None':
            msg = self.input_check().extended_diag(
                err_txt='Пожалуйста, выберите действие:', buttons=[
                    'Отвязать телеграм', 'Открыть бота'])
            if msg == True:
                self.timedb.set_logged_user_data(item='del_telegram')
                self.input_check().simple_diag('Телеграм успешно отвязан!')
                self.sUi.settings_imglbl_telegram_noverify.setHidden(False)
                self.timedb.get_logged_user_data(
                    item='get_user_telegram')
            elif msg == False:
                webbrowser.open_new_tab(
                    'https://t.me/TimeSoft_Assistant_Bot')
                return
        else:
            webbrowser.open_new_tab(
                'https://t.me/TimeSoft_Assistant_Bot')
            return

    def view_table(self):
        rows = self.timedb.get_logged_user_data(
            item='get_user_activities_table')
        self.ttUi.tableW.setRowCount(len(rows))

        self.ttUi.tableW.setSortingEnabled(False)
        x = 0
        for row in rows:
            row3 = self.input_check().secondsToText(int(row[3])*60)

            if not row[5] == None and not row[5] == '' and not row[5] == '(NULL)':
                row[2] = f'{row[2]}*'

            # self.ttUi.tableW.horizontalHeader().sortIndicatorOrder()
            self.ttUi.tableW.setItem(
                x, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.ttUi.tableW.setItem(
                x, 1, QtWidgets.QTableWidgetItem(row[4]))
            self.ttUi.tableW.setItem(
                x, 2, QtWidgets.QTableWidgetItem(row[1]))
            self.ttUi.tableW.setItem(
                x, 3, QtWidgets.QTableWidgetItem(row[2]))
            self.ttUi.tableW.setItem(
                # 'row3' is valid.
                x, 4, QtWidgets.QTableWidgetItem(row3))
            self.ttUi.tableW.setItem(
                x, 5, QtWidgets.QTableWidgetItem(row[5]))
            x += 1

        self.ttUi.tableW.setSortingEnabled(True)
        self.ttUi.tableW.sortItems(1, Qt.DescendingOrder)
        self.ttUi.tableW.resizeColumnsToContents()
        self.lay.addWidget(self.ttUi.tableW)

    def update_view_table(self, date=None, custom_date=None, category=None):
        # self.lay.removeWidget(self.tUi)
        # self.tUi.tableW.setParent(None) # Removing tUi widget from wUi.
        for i in reversed(range(self.lay.count())):
            self.lay.itemAt(i).widget().setParent(None)

        if date == None and custom_date == None:
            rows = self.timedb.get_logged_user_data(
                item='get_user_activities_table')
        elif not date == None and custom_date == None:
            rows = self.timedb.set_logged_user_data(
                item='set_user_activities_table',
                add_params=['single_date'], edit_params=[date])
        elif not date == None and not custom_date == None:
            rows = self.timedb.set_logged_user_data(
                item='set_user_activities_table',
                add_params=['custom_date'], edit_params=[custom_date, date])
        if date == None and custom_date == None and not category == None:
            rows = self.timedb.set_logged_user_data(
                item='set_user_activities_table',
                add_params=['cat_name'], edit_params=[category])

        self.ttUi.tableW.setRowCount(len(rows))

        self.ttUi.tableW.setSortingEnabled(False)
        x = 0
        for row in rows:
            row3 = self.input_check().secondsToText(int(row[3])*60)

            if not row[5] == None and not row[5] == '' and not row[5] == '(NULL)':
                row[2] = f'{row[2]}*'

            self.ttUi.tableW.horizontalHeader().sortIndicatorOrder()
            self.ttUi.tableW.setItem(
                x, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.ttUi.tableW.setItem(
                x, 1, QtWidgets.QTableWidgetItem(row[4]))
            self.ttUi.tableW.setItem(
                x, 2, QtWidgets.QTableWidgetItem(row[1]))
            self.ttUi.tableW.setItem(
                x, 3, QtWidgets.QTableWidgetItem(row[2]))
            self.ttUi.tableW.setItem(
                x, 4, QtWidgets.QTableWidgetItem(row3))
            self.ttUi.tableW.setItem(
                x, 5, QtWidgets.QTableWidgetItem(row[5]))
            x += 1

        self.ttUi.tableW.setSortingEnabled(True)
        self.ttUi.tableW.sortItems(1, Qt.DescendingOrder)
        self.ttUi.tableW.resizeColumnsToContents()
        self.lay.addWidget(self.ttUi.tableW)

    def view_table_sort_by_day(self):
        self.update_view_table(self.today.strftime('%Y-%m-%d'))

    def view_table_sort_by_week(self):
        new = self.today.replace(day=self.today.day - 7)
        self.update_view_table(
            date=self.today.strftime('%Y-%m-%d'), custom_date=new.strftime('%Y-%m-%d'))

    def view_table_sort_by_month(self):
        new = self.today.replace(month=self.today.month - 1)
        self.update_view_table(
            date=self.today.strftime('%Y-%m-%d'), custom_date=new.strftime('%Y-%m-%d'))

    def view_table_sort_by_year(self):
        new = self.today.replace(year=self.today.year - 1)
        self.update_view_table(
            date=self.today.strftime('%Y-%m-%d'), custom_date=new.strftime('%Y-%m-%d'))

    def view_table_custom_sort(self):
        date_from = self.mUi.mainwindow_dateEdit_s.date().toString('yyyy-MM-dd')
        date_to = self.mUi.mainwindow_dateEdit_po.date().toString('yyyy-MM-dd')
        self.update_view_table(date=date_to, custom_date=date_from)

    def view_table_clear_filter(self):
        self.update_view_table()

    def view_categ(self):
        # Layout creation for viewing various data in it.
        self.categ_lay = QtWidgets.QGridLayout()
        self.categ_lay.setRowStretch(100, 1)

        lbl = QtWidgets.QLabel('КАТЕГОРИИ')
        lbl.setStyleSheet("""
        QLabel {
            font-family: "Roboto", Light;
            font-size: 12pt;
            margin-top: 7px;
            margin-left: 10px;}
        """)
        lbl.setGeometry(1, 7, 159, 23)

        btn = QtWidgets.QPushButton('—')
        btn.setStyleSheet("""
        QPushButton {
            font-family: "Roboto", Light;
            font-size: 14pt;
            background-color: rgba(0, 0, 0, 0);
            color: rgb(255, 255, 255);
            border: 2px solid rgb(115, 103, 240);
            border-radius: 5px;
            width: 100px;
            height: 30px;
            margin-top: 3px;
        }
        QPushButton:hover {
            background-color: rgb(115, 103, 240);
            color: rgb(255, 255, 255);
            border: 1px solid rgb(115, 103, 240);}
        """)
        btn.setGeometry(166, 1, 100, 30)

        btn.clicked.connect(self.cUi.show)

        self.categ_lay.addWidget(lbl, 0, 0, alignment=Qt.AlignLeft)
        self.categ_lay.addWidget(btn, 0, 1, alignment=Qt.AlignRight)

        self.view_all = QtWidgets.QRadioButton(
            'Посмотреть все', clicked=self.view_table_sort_by_category)
        self.view_all.setStyleSheet("""
            QRadioButton {
                font-family: "Roboto", Light;
                font-size: 12pt;
                margin-top: 7px;
                margin-left: 5px;}
            """)
        self.view_all.setChecked(True)
        self.view_all.setObjectName('Посмотреть все')

        all_overall_time = self.timedb.set_logged_user_data(
            item='get_category_overall_time', add_params=['all'])

        if all_overall_time == 'None':
            all_overall_time = ''
        else:
            all_overall_time = self.input_check().secondsToText(
                int(all_overall_time)*60, 'categs')

        lbl_time = QtWidgets.QLabel(f'{all_overall_time}')
        lbl_time.setStyleSheet("""
        QLabel {
            font-family: "Roboto", Light;
            font-size: 12pt;
            margin-top: 7px;}
        """)

        self.categ_lay.addWidget(self.view_all, 1, 0, alignment=Qt.AlignLeft)
        self.categ_lay.addWidget(lbl_time, 1, 1, alignment=Qt.AlignRight)

        i = 2
        categs = self.timedb.get_logged_user_data(item='get_user_categories')

        for row in categs:
            overall_time = self.timedb.set_logged_user_data(
                item='get_category_overall_time', add_params=[row])

            if overall_time == 'None':
                all_overall_time = ''
            else:
                overall_time = self.input_check().secondsToText(
                    int(overall_time)*60, 'categs')

            self.radiobutton = QtWidgets.QRadioButton(
                row, clicked=self.view_table_sort_by_category)
            self.radiobutton.setStyleSheet("""
            QRadioButton {
                font-family: "Roboto", Light;
                font-size: 12pt;
                margin-top: 7px;
                margin-left: 5px;}
            """)
            self.radiobutton.setObjectName(row)

            lbl_time = QtWidgets.QLabel(f'{overall_time}')
            lbl_time.setStyleSheet("""
            QLabel {
                font-family: "Roboto", Light;
                font-size: 12pt;
                margin-top: 7px;}
            """)

            self.categ_lay.addWidget(
                self.radiobutton, i, 0, alignment=Qt.AlignLeft)
            if lbl_time.text() == 'None':
                pass
            else:
                self.categ_lay.addWidget(
                    lbl_time, i, 1, alignment=Qt.AlignRight)

            i += 1

        self.ccUi.setLayout(self.categ_lay)

    def update_view_categ(self):
        for i in range(self.categ_lay.count()):
            self.categ_lay.itemAt(i).widget().deleteLater()

        lbl = QtWidgets.QLabel('КАТЕГОРИИ')
        lbl.setStyleSheet("""
        QLabel {
            font-family: "Roboto", Light;
            font-size: 12pt;
            margin-top: 7px;
            margin-left: 10px;}
        """)
        lbl.setGeometry(1, 7, 159, 23)

        btn = QtWidgets.QPushButton('—')
        btn.setStyleSheet("""
        QPushButton {
            font-family: "Roboto", Light;
            font-size: 14pt;
            background-color: rgba(0, 0, 0, 0);
            color: rgb(255, 255, 255);
            border: 2px solid rgb(115, 103, 240);
            border-radius: 5px;
            width: 100px;
            height: 30px;
            margin-top: 3px;
        }
        QPushButton:hover {
            background-color: rgb(115, 103, 240);
            color: rgb(255, 255, 255);
            border: 1px solid rgb(115, 103, 240);}
        """)
        btn.setGeometry(166, 1, 100, 30)

        btn.clicked.connect(self.cUi.show)

        self.categ_lay.addWidget(lbl, 0, 0, alignment=Qt.AlignLeft)
        self.categ_lay.addWidget(btn, 0, 1, alignment=Qt.AlignRight)

        self.view_all = QtWidgets.QRadioButton(
            'Посмотреть все', clicked=self.view_table_sort_by_category)
        self.view_all.setStyleSheet("""
            QRadioButton {
                font-family: "Roboto", Light;
                font-size: 12pt;
                margin-top: 7px;
                margin-left: 5px;}
            """)
        self.view_all.setChecked(True)
        self.view_all.setObjectName('Посмотреть все')

        all_overall_time = self.timedb.set_logged_user_data(
            item='get_category_overall_time', add_params=['all'])

        if all_overall_time == 'None':
            all_overall_time = ''
        else:
            all_overall_time = self.input_check().secondsToText(
                int(all_overall_time)*60, 'categs')

        lbl_time = QtWidgets.QLabel(f'{all_overall_time}')
        lbl_time.setStyleSheet("""
        QLabel {
            font-family: "Roboto", Light;
            font-size: 12pt;
            margin-top: 7px;}
        """)

        self.categ_lay.addWidget(self.view_all, 1, 0, alignment=Qt.AlignLeft)
        self.categ_lay.addWidget(lbl_time, 1, 1, alignment=Qt.AlignRight)

        i = 2
        categs = self.timedb.get_logged_user_data(item='get_user_categories')

        for row in categs:
            overall_time = self.timedb.set_logged_user_data(
                item='get_category_overall_time', add_params=[row])

            if overall_time == 'None':
                pass
            else:
                overall_time = self.input_check().secondsToText(
                    int(overall_time)*60, 'categs')

            self.radiobutton = QtWidgets.QRadioButton(
                row, clicked=self.view_table_sort_by_category)
            self.radiobutton.setStyleSheet("""
            QRadioButton {
                font-family: "Roboto", Light;
                font-size: 12pt;
                margin-top: 7px;
                margin-left: 5px;}
            """)
            self.radiobutton.setObjectName(row)

            lbl_time = QtWidgets.QLabel(f'{overall_time}')
            lbl_time.setStyleSheet("""
            QLabel {
                font-family: "Roboto", Light;
                font-size: 12pt;
                margin-top: 7px;}
            """)

            self.categ_lay.addWidget(
                self.radiobutton, i, 0, alignment=Qt.AlignLeft)
            if lbl_time.text() == 'None':
                pass
            else:
                self.categ_lay.addWidget(
                    lbl_time, i, 1, alignment=Qt.AlignRight)

            i += 1

    def view_table_sort_by_category(self):
        sender = self.radiobutton.sender()
        name = sender.objectName()

        if self.view_all.isChecked() == True:
            self.update_view_table()
        else:
            self.update_view_table(category=name)

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
            (set([x for x in self.categories if self.categories.count(x) >= 1])))

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
            for i in range(self.lay.count()):
                self.lay.itemAt(i).widget().setParent(None)

            self.lay.addWidget(self.ttUi.tableW)

        # Displaying the diagram/chart if combobox current index is equal to 1.
        elif self.mUi.mainwindow_comboBox_display_style.currentIndex() == 1:
            # Removing all widgets from layout.
            for i in range(self.lay.count()):
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
            for i in range(self.lay.count()):
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

    def help(self):
        webbrowser.open_new_tab(
            'https://doc.qt.io/qtforpython/#documentation')
        webbrowser.open_new_tab(
            'https://docs.python.org/3/')
        webbrowser.open_new_tab(
            'http://timesoft.pp.ua/')


# ----------------------------------------------------------END-----timeSoft.py

# ----------------------------------------------------------START----dblogic.py


class DbLogic:
    """
    The DbLogic class impelements configuration and connection to the
    PostgreSql database.

    There are 4 methods in total:
    - user registration
    - user login
    - getting data from logged user
    - setting data for logged user
    """

    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8-sig')

    def __init__(self):

        self.connection = db.connect(
            self.config.get('PostgreSql', 'DATABASE_URL'))

        self.cursor = self.connection.cursor()
        self.cursor2 = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)

        self.correct_login_info = False
        self.user_input_check = None
        self.current_import_status = 0

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

            self.cursor.execute(
                'INSERT INTO "USER_PRIVATE" (user_p_id, user_p_email, user_p_password)\
                VALUES (%s,%s,%s) ON CONFLICT DO NOTHING', (
                    user_p_id, user_p_email, user_p_password))
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
                (user_id, actl_name, cat_name) = (\
                    \'{self.user_id}\', \'{params[1]}\', \'{params[0]}\')')
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

        # For getting user activities_list.
        elif item == 'get_user_activity_list':
            self.cursor2.execute(
                f'SELECT actl_name, cat_name FROM "ACTIVITY_LIST" WHERE\
                    user_id = \'{self.user_id}\'')
            user_activity_list = []
            for row in self.cursor2.fetchall():
                user_activity_list.append(row)
            return user_activity_list

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

        elif item == 'get_user_activities_table':
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
                user_activities.append(row)
            return user_activities

        elif item == 'get_user_telegram':
            self.cursor.execute(
                f'SELECT user_n_telegram FROM "USER_NAME" WHERE user_n_id = {self.user_n_id}')
            return str(self.cursor.fetchall())[2:-3]

    def set_logged_user_data(
            self, user_login=None, item=None, add_params=None, edit_params=None):
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

        elif item == 'get_act_time':
            self.cursor.execute(
                f'SELECT act_time FROM "ACTIVITY" WHERE\
                    act_id = \'{add_params[0]}\' and user_id = \'{self.user_id}\'')
            return str(self.cursor.fetchall())[2:-3]

        elif item == 'set_default_categs_and_activities':
            self.cursor.execute(
                f'INSERT INTO "CATEGORY" (user_id, cat_name) VALUES\
                    (%s,%s) ON CONFLICT DO NOTHING',
                (self.user_id, add_params[0]))

            self.connection.commit()

            self.cursor.execute(
                f'INSERT INTO "ACTIVITY_LIST" (\
                    user_id, actl_name, cat_name) VALUES\
                        (%s,%s,%s) ON CONFLICT DO NOTHING',
                (self.user_id, add_params[1], add_params[0]))

            self.connection.commit()

        # Adding event as itself.
        elif item == 'add_event':
            # Updating CATEGORY table, if there are no matching data.
            self.cursor.execute(
                f'INSERT INTO "CATEGORY" (user_id, cat_name) VALUES\
                    (%s,%s) ON CONFLICT DO NOTHING',
                (self.user_id, add_params[0]))

            self.connection.commit()

            # Updating ACTIVITY_LIST table also, if there are no matching data.
            self.cursor.execute(
                f'INSERT INTO "ACTIVITY_LIST" (\
                    user_id, actl_name, cat_name) VALUES\
                        (%s,%s,%s) ON CONFLICT DO NOTHING',
                (self.user_id, add_params[1], add_params[0]))

            self.connection.commit()

            self.cursor2.execute('INSERT INTO "ACTIVITY" (user_id, actl_name,\
                        act_time, act_date, cat_name, act_comment)\
                            VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING',
                                 (self.user_id, add_params[1], add_params[2],
                                  add_params[3], add_params[0], add_params[4]))

            self.connection.commit()

        # Editing existing event in db.
        elif item == 'edit_event':
            # Updating CATEGORY table, if there are no matching data.
            self.cursor.execute(
                f'INSERT INTO "CATEGORY" (user_id, cat_name) VALUES\
                    (%s,%s) ON CONFLICT DO NOTHING',
                (self.user_id, edit_params[0]))

            self.connection.commit()

            # Updating ACTIVITY_LIST table also, if there are no matching data.
            self.cursor.execute(
                f'INSERT INTO "ACTIVITY_LIST" (\
                    user_id, actl_name, cat_name) VALUES\
                        (%s,%s,%s) ON CONFLICT DO NOTHING',
                (self.user_id, edit_params[1], edit_params[0]))

            self.connection.commit()

            self.cursor2.execute(
                f'UPDATE "ACTIVITY" SET (actl_name, act_time, act_date, cat_name, \
                    act_comment) = (\
                        \'{edit_params[1]}\', \'{edit_params[2]}\', \'{edit_params[3]}\',\
                            \'{edit_params[0]}\', \'{edit_params[4]}\')\
                            WHERE act_id = \'{add_params[5]}\'')

            self.connection.commit()

        # Deleting existing event.
        elif item == 'del_event':
            self.cursor.execute(
                f'DELETE FROM "ACTIVITY" WHERE act_id = \'{add_params[2]}\'')

            self.connection.commit()

            self.cursor2.execute(
                f'SELECT count(cat_name), count(actl_name) FROM "ACTIVITY" WHERE\
                    user_id = \'{self.user_id}\' and cat_name = \'{add_params[0]}\' and\
                        actl_name = \'{add_params[1]}\'')
            activity_cat_actl_name = self.cursor2.fetchall()
            for row in activity_cat_actl_name:
                if row[0] == 0 and row[1] == 0:
                    print(row)
                    self.cursor.execute(
                        f'DELETE FROM "ACTIVITY_LIST" WHERE\
                            user_id = \'{self.user_id}\' and\
                                actl_name = \'{add_params[1]}\'\
                                    and cat_name = \'{add_params[0]}\'')

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

        elif item == 'import_add':
            for row in edit_params:
                try:
                    self.cursor.execute(
                        f'INSERT INTO "CATEGORY" (user_id, cat_name) VALUES\
                            (\'{self.user_id}\', \'{row[0]}\') ON CONFLICT DO NOTHING')

                    self.cursor.execute(
                        f'INSERT INTO "ACTIVITY_LIST" (user_id, actl_name, cat_name) VALUES\
                            (\'{self.user_id}\', \'{row[1]}\', \'{row[0]}\') ON CONFLICT DO NOTHING')

                    self.cursor.execute(
                        f'INSERT INTO "ACTIVITY"\
                            (user_id, actl_name, act_time, act_date, cat_name, \
                            act_comment) VALUES\
                                (\'{self.user_id}\', \'{row[1]}\', \'{row[2]}\',\
                                \'{row[3]}\',\'{row[0]}\', \'{row[4]}\') ON CONFLICT DO NOTHING')
                    self.current_import_status = len(edit_params)
                except Exception as e:
                    if isinstance(e, db.DatabaseError):
                        print(e)
                        break

            self.connection.commit()

        elif item == 'import_rewrite':
            for row in edit_params:
                self.current_import_status = len(row)

        # Deleting telegram reference.
        elif item == 'del_telegram':
            self.cursor2.execute(
                f'UPDATE "USER_NAME" SET user_n_telegram = NULL\
                    WHERE user_n_id = {self.user_n_id}')

            self.connection.commit()

        elif item == 'del_user_categ':
            self.cursor.execute(
                f'DELETE FROM "CATEGORY" WHERE\
                    user_id = \'{self.user_id}\' and cat_name = \'{add_params[0]}\'')

            self.connection.commit()

        elif item == 'set_user_activities_table':
            if add_params[0] == 'single_date':
                self.cursor2.execute(
                    f'SELECT act_id, cat_name, actl_name, act_time, act_date, act_comment\
                        FROM "ACTIVITY" WHERE user_id = \'{self.user_id}\' and\
                            act_date = \'{edit_params[0]}\'')
                user_activities = []
                for row in self.cursor2.fetchall():
                    # Setting date in str fromat.
                    date_ = row[4].strftime('%Y-%m-%d')
                    row[4] = date_
                    # Setting duration in str fromat.
                    duration = str(row[3])
                    row[3] = duration
                    user_activities.append(row)
                return user_activities

            elif add_params[0] == 'custom_date':
                self.cursor2.execute(
                    f'SELECT act_id, cat_name, actl_name, act_time, act_date, act_comment\
                        FROM "ACTIVITY" WHERE user_id = \'{self.user_id}\' and\
                            act_date BETWEEN \'{edit_params[0]}\' and \'{edit_params[1]}\'')
                user_activities = []
                for row in self.cursor2.fetchall():
                    # Setting date in str fromat.
                    date_ = row[4].strftime('%Y-%m-%d')
                    row[4] = date_
                    # Setting duration in str fromat.
                    duration = str(row[3])
                    row[3] = duration
                    user_activities.append(row)
                return user_activities

            elif add_params[0] == 'cat_name':
                self.cursor2.execute(
                    f'SELECT act_id, cat_name, actl_name, act_time, act_date, act_comment\
                        FROM "ACTIVITY" WHERE user_id = \'{self.user_id}\' and\
                            cat_name = \'{edit_params[0]}\'')
                user_activities = []
                for row in self.cursor2.fetchall():
                    # Setting date in str fromat.
                    date_ = row[4].strftime('%Y-%m-%d')
                    row[4] = date_
                    # Setting duration in str fromat.
                    duration = str(row[3])
                    row[3] = duration
                    user_activities.append(row)
                return user_activities

        elif item == 'get_category_overall_time':
            if add_params[0] == 'all':
                self.cursor2.execute(
                    f'SELECT SUM(act_time) FROM "ACTIVITY" WHERE\
                        user_id = \'{self.user_id}\'')
                overall_time_for_category = str(self.cursor2.fetchall())[2:-2]
                return overall_time_for_category
            else:
                self.cursor2.execute(
                    f'SELECT SUM(act_time) FROM "ACTIVITY" WHERE\
                        user_id = \'{self.user_id}\' and cat_name = \'{add_params[0]}\'')
                overall_time_for_category = str(self.cursor2.fetchall())[2:-2]
                return overall_time_for_category


class StyleSheets:
    def __init__(self):
        # Loading UI interfaces.
        self.mUi = uic.loadUi('design\\mainwindow_d.ui')  # Main window ui.
        self.aUi = uic.loadUi('design\\add_event_d.ui')  # Add actions ui.
        self.eUi = uic.loadUi('design\\edit_event_d.ui')  # Edit actions ui.
        self.cUi = uic.loadUi('design\\category_delete.ui')  # Category del ui.
        self.rUi = uic.loadUi('design\\register_d.ui')  # Registration win ui.
        self.lUi = uic.loadUi('design\\login_d.ui')  # Login window ui.
        self.sUi = uic.loadUi('design\\settings_d.ui')  # Settings window ui.
        self.ttUi = uic.loadUi('design\\table.ui')  # Table ui.
        self.abUi = uic.loadUi('design\\about_us_d.ui')  # About us ui.

        # Widget for viewing various data.
        # Viewing widget in the right side.
        self.wUi = self.mUi.mainwindow_widget_view

        # Widget for viewing user categories.
        self.ccUi = self.mUi.mainwindow_widget_category
        self.scroll_ccUi = self.mUi.scrollArea

        self.status = None

    def dark_theme(self):
        bgcol_distant = '#283046'
        bgcol_middle = '#161D31'
        bgcol_transparent = 'rgba(0, 0, 0, 0)'

        color_white = '#FFFFFF'
        color_theme = '#5F55C8'
        color_default = '#7367F0'
        color_disabled = 'rgba(115, 103, 240, 0.38)'
        color_active = '#5E50EE'
        color_black = '#000000'
        color_border = '#404656'
        color_name = '#D0D2D6'
        color_text = '#676D7D'
        color_1 = '#6E6B7B'
        color_theme = '#796DFF'
        color_3 = '#EA5455'
        color_4 = '#7A7A7A'
        color_5 = '#3B4253'

        color_hover_1 = '#B4B7BD'
        color_hover_2 = '#7666F8'

        about_us_border = 'border: 2px solid #CE2745; border-radius: 50px;'

        # ----------------------------------------------------------------
        # Login CSS style. Dark.
        self.lUi.setStyleSheet(
            f'background-color: {bgcol_middle};'
        )
        self.lUi.login_text_logo.setStyleSheet(
            f'color: {color_default};'
        )
        self.lUi.login_widget.setStyleSheet(
            f'background-color: {bgcol_distant};'
        )
        self.lUi.login_btn_create_account.setStyleSheet(
            """QPushButton {"""
            f'color: {color_disabled};'
            f'background-color: {bgcol_transparent};'
            """}
            QPushButton::hover {"""
            f'color: {color_hover_1};'
            """}"""
        )
        self.lUi.login_btn_login.setStyleSheet(
            """QPushButton {"""
            f'background-color: {color_default};'
            f'border-radius: 5px;'
            f'border: 2px solid {color_default};'
            f'color: {color_white};'
            """}
            QPushButton::hover {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_white};'
            f'border: 2px solid {color_active};'
            """}"""
        )
        self.lUi.login_btn_theme.setStyleSheet(
            f'background-color: {bgcol_transparent};'
        )
        self.lUi.login_lineedit_email.setStyleSheet(
            """QLineEdit {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_text};'
            f'border: 1px solid {color_border};'
            f'border-radius: 5px;'
            f'padding-left: 15px;'
            """}
            QLineEdit::hover {"""
            f'border: 1px solid {color_active};'
            """}"""
        )
        self.lUi.login_lineedit_password.setStyleSheet(
            """QLineEdit {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_text};'
            f'border: 1px solid {color_border};'
            f'border-radius: 5px;'
            f'padding-left: 15px;'
            """}
            QLineEdit::hover {"""
            f'border: 1px solid {color_active};'
            """}"""
        )
        self.lUi.login_text_account.setStyleSheet(
            f'color: {color_1};'
        )
        self.lUi.login_text_email.setStyleSheet(
            f'color: {color_hover_1};'
        )
        self.lUi.login_text_paragrah_log.setStyleSheet(
            f'color: {color_name};'
        )
        self.lUi.login_text_password.setStyleSheet(
            f'color: {color_hover_1};'
        )
        self.lUi.login_text_title.setStyleSheet(
            f'color: {color_name};'
        )
        # ----------------------------------------------------------------
        # Register CSS style. Dark.
        self.rUi.setStyleSheet(
            f'background-color: {bgcol_middle};'
        )
        self.rUi.register_txtlbl_logo.setStyleSheet(
            f'color: {color_default};'
        )
        self.rUi.register_widget.setStyleSheet(
            f'background-color: {bgcol_distant};'
        )
        self.rUi.register_btn_create.setStyleSheet(
            """QPushButton {"""
            f'color: {color_disabled};'
            f'background-color: {bgcol_transparent};'
            """}
            QPushButton::hover {"""
            f'color: {color_hover_1};'
            """}"""
        )
        self.rUi.register_btn_login.setStyleSheet(
            """QPushButton {"""
            f'background-color: {color_default};'
            f'border-radius: 5px;'
            f'border: 2px solid {color_default};'
            f'color: {color_white};'
            """}
            QPushButton::hover {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_white};'
            f'border: 2px solid {color_active};'
            """}"""
        )
        self.rUi.register_checkbox_agree.setStyleSheet(
            f'color: {color_name};'
        )
        self.rUi.register_lineEdit_email.setStyleSheet(
            """QLineEdit {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_text};'
            f'border: 1px solid {color_border};'
            f'border-radius: 5px;'
            f'padding-left: 15px;'
            """}
            QLineEdit::hover {"""
            f'border: 1px solid {color_active};'
            """}"""
        )
        self.rUi.register_lineEdit_name.setStyleSheet(
            """QLineEdit {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_text};'
            f'border: 1px solid {color_border};'
            f'border-radius: 5px;'
            f'padding-left: 15px;'
            """}
            QLineEdit::hover {"""
            f'border: 1px solid {color_active};'
            """}"""
        )
        self.rUi.register_lineEdit_password.setStyleSheet(
            """QLineEdit {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_text};'
            f'border: 1px solid {color_border};'
            f'border-radius: 5px;'
            f'padding-left: 15px;'
            """}
            QLineEdit::hover {"""
            f'border: 1px solid {color_active};'
            """}"""
        )
        self.rUi.register_txtlbl_email.setStyleSheet(
            f'color: {color_hover_1};'
        )
        self.rUi.register_txtlbl_name.setStyleSheet(
            f'color: {color_hover_1};'
        )
        self.rUi.register_txtlbl_password.setStyleSheet(
            f'color: {color_hover_1};'
        )
        self.rUi.register_txtlbl_pragrah_log.setStyleSheet(
            f'color: {color_name};'
        )
        self.rUi.register_txtlbl_reg.setStyleSheet(
            f'color: {color_1};'
        )
        self.rUi.register_txtlbl_title.setStyleSheet(
            f'color: {color_name};'
        )
        # ----------------------------------------------------------------
        # Main UI. Dark.
        self.mUi.setStyleSheet(
            f'background-color: {bgcol_middle};'
        )
        self.mUi.mainwindow_widget_category.setStyleSheet(
            """QWidget {"""
            f'color: {color_name};'
            f'background-color: {bgcol_distant};'
            f'border-top-left-radius: 5px;'
            f'border-bottom-left-radius: 5px;'
            """}"""
        )
        self.mUi.mainwindow_widget_navigation.setStyleSheet(
            """QWidget {"""
            f'background-color: {bgcol_distant};'
            f'border-radius: 5px;'
            """}"""
        )
        self.mUi.mainwindow_btn_all.setStyleSheet(
            """QPushButton {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_white};'
            f'border: 2px solid {color_theme};'
            f'border-top-left-radius: 0;'
            f'border-top-right-radius: 5px;'
            f'border-bottom-right-radius: 5px;'
            f'border-bottom-left-radius: 0;'
            f'padding-left: 20px;'
            f'padding-right: 20px;'
            """}
            QPushButton::hover {"""
            f'border: 2px solid {color_active};'
            f'border-top-left-radius: 0;'
            f'border-top-right-radius: 5px;'
            f'border-bottom-right-radius: 5px;'
            f'border-bottom-left-radius: 0;'
            """}"""
        )
        self.mUi.mainwindow_btn_annually.setStyleSheet(
            """QPushButton {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_white};'
            f'border: 2px solid {color_theme};'
            f'border-right: 0;'
            f'border-radius: 0;'
            f'padding-left: 20px;'
            f'padding-right: 20px;'
            """}
            QPushButton::hover {"""
            f'border: 2px solid {color_active};'
            f'border-radius: 0;'
            """}"""
        )
        self.mUi.mainwindow_btn_daily.setStyleSheet(
            """QPushButton {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_white};'
            f'border: 2px solid {color_theme};'
            f'border-top-left-radius: 5px;'
            f'border-top-right-radius: 0;'
            f'border-bottom-right-radius: 0;'
            f'border-bottom-left-radius: 5px;'
            f'padding-left: 20px;'
            f'padding-right: 20px;'
            """}
            QPushButton::hover {"""
            f'border: 2px solid {color_active};'
            f'border-top-left-radius: 5px;'
            f'border-top-right-radius: 0;'
            f'border-bottom-right-radius: 0;'
            f'border-bottom-left-radius: 5px;'
            """}"""
        )
        self.mUi.mainwindow_btn_monthly.setStyleSheet(
            """QPushButton {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_white};'
            f'border: 2px solid {color_theme};'
            f'border-right: 0;'
            f'border-radius: 0;'
            f'padding-left: 20px;'
            f'padding-right: 20px;'
            """}
            QPushButton::hover {"""
            f'border: 2px solid {color_active};'
            f'border-radius: 0;'
            """}"""
        )
        self.mUi.mainwindow_btn_nav_add_act.setStyleSheet(
            """QPushButton {"""
            f'background-color: {color_default};'
            f'color: {color_white};'
            f'border: 2px solid {color_default};'
            f'border-radius: 5px;'
            f'padding-left: 12px;'
            f'padding-right: 12px;'
            f'padding-top: 5px;'
            f'padding-bottom: 5px;'
            """}
            QPushButton::hover {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_default};'
            f'border: 2px solid {color_default};'
            """}"""
        )
        self.mUi.mainwindow_btn_weekly.setStyleSheet(
            """QPushButton {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_white};'
            f'border: 2px solid {color_theme};'
            f'border-right: 0;'
            f'border-radius: 0;'
            f'padding-left: 20px;'
            f'padding-right: 20px;'
            """}
            QPushButton::hover {"""
            f'border: 2px solid {color_active};'
            f'border-radius: 0;'
            """}"""
        )
        self.mUi.mainwindow_dateEdit_po.setStyleSheet(
            """QDateEdit {"""
            f'background-color: {bgcol_distant};'
            f'border-radius: 5px;'
            f'color: {color_white};'
            f'margin-right: 5px;'
            """}
            QDateEdit::hover {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_white};'
            """}"""
        )
        self.mUi.mainwindow_dateEdit_s.setStyleSheet(
            """QDateEdit {"""
            f'background-color: {bgcol_distant};'
            f'border-radius: 5px;'
            f'color: {color_white};'
            """}
            QDateEdit::hover {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_white};'
            """}"""
        )
        self.mUi.mainwindow_lbl_icon_clendar.setStyleSheet(
            f'margin-left: 20px;'
            f'color: {color_name};'
            f'padding-top: 4px;'
            f'padding-bottom: 4px;'
        )
        self.mUi.mainwindow_textlbl_po.setStyleSheet(
            f'padding-left: 5px;'
            f'padding-right: 5px;'
            f'color: {color_name};'
        )
        self.mUi.mainwindow_textlbl_s.setStyleSheet(
            f'padding-left: 5px;'
            f'padding-right: 5px;'
            f'color: {color_name};'
        )
        self.mUi.mainwindow_widget_view.setStyleSheet(
            f'background-color: {bgcol_distant};'
            f'background-image: url(design/img/background-image_d.png);'
        )
        self.mUi.mainwindow_widget_view_spacer.setStyleSheet(
            f'border-right: 1px solid  {color_5};'
            f'background-color: {bgcol_distant};'
        )
        self.mUi.mainwindow_widget_logo.setStyleSheet(
            f'background-color: {bgcol_distant};'
        )
        self.mUi.mainwindow_lbl_logo_title.setStyleSheet(
            f'color: {color_default};'
        )
        self.mUi.mainwindow_widget_menu.setStyleSheet(
            f'background-color: {bgcol_distant};'
        )
        self.mUi.mainwindow_btn_exit.setStyleSheet(
            """QPushButton {"""
            f'background-color: {bgcol_transparent};'
            f'color: {color_name};'
            f'text-align: left;'
            f'padding-right: 10px;'
            """}
            QPushButton::hover {"""
            f'background-color: {bgcol_transparent};'
            f'color: {color_theme};'
            """}"""
        )
        self.mUi.mainwindow_btn_forecast.setStyleSheet(
            """QPushButton {"""
            f'background-color: {bgcol_transparent};'
            f'color: {color_name};'
            f'text-align: left;'
            f'padding-right: 10px;'
            f'margin-top: 27px;'
            """}
            QPushButton::hover {"""
            f'background-color: {bgcol_transparent};'
            f'color: {color_theme};'
            """}"""
        )
        self.mUi.mainwindow_btn_settings.setStyleSheet(
            """QPushButton {"""
            f'background-color: {bgcol_transparent};'
            f'color: {color_name};'
            f'text-align: left;'
            f'padding-right: 10px;'
            """}
            QPushButton::hover {"""
            f'background-color: {bgcol_transparent};'
            f'color: {color_theme};'
            """}"""
        )
        self.mUi.mainwindow_btn_theme.setStyleSheet(
            """QPushButton {"""
            f'background-color: {bgcol_transparent};'
            f'color: {color_name};'
            f'text-align: left;'
            f'padding-right: 10px;'
            """}
            QPushButton::hover {"""
            f'background-color: {bgcol_transparent};'
            f'color: {color_theme};'
            """}"""
        )
        self.mUi.mainwindow_comboBox_display_style.setStyleSheet(
            """QComboBox {"""
            f'font: 12pt;'
            f'background-color: {bgcol_middle};'
            f'color: {color_name};'
            f'border: 2px solid {bgcol_transparent};'
            f'border-radius: 5px;'
            f'padding-left: 10px;'
            """}
            QComboBox::hover {"""
            f'background-color: {bgcol_middle};'
            f'color: {color_hover_2};'
            f'border: 2px solid  {color_hover_2};'
            f'border-radius: 5px;'
            """}
            QComboBox QAbstractItemView {"""
            f'background-color: {bgcol_middle};'
            f'border: 2px solid  {color_hover_2};'
            f'color: #CBCBCB;'
            f'selection-background-color: {color_active};'
            f'selection-color: {color_black};'
            f'border-top-left-radius: 0;'
            f'border-top-right-radius: 0;'
            f'border-bottom-right-radius: 5px;'
            f'border-bottom-left-radius: 5px;'
            """}"""
        )
        self.mUi.mainwindow_textlbl_display_style.setStyleSheet(
            f'color: {color_name};'
            f'margin-top: 20px;'
        )
        self.mUi.mainwindow_menubar.setStyleSheet(
            """QMenuBar {"""
            f'color: #CBCBCB;'
            f'background-color: rgba(0, 0, 0, 130);'
            """}
            QMenuBar::item:selected {"""
            f'background-color: #C8C8C8;'
            f'color: {color_black};'
            """}
            QMenuBar::item:pressed {"""
            f'background-color: #C8C8C8;'
            f'color: {color_black};'
            """}"""
        )
        self.mUi.mainwindow_menuFile.setStyleSheet(
            """QMenu {"""
            f'background-color: #141822;'
            f'color: #CBCBCB;'
            """}
            QMenu::item:selected {"""
            f'background-color: #C8C8C8;'
            f'color: {color_black};'
            """}
            QMenu::item:pressed {"""
            f'background-color: #C8C8C8;'
            f'color: {color_black};'
            """}"""
        )
        self.mUi.mainwindow_menuEdit.setStyleSheet(
            """QMenu {"""
            f'background-color: #141822;'
            f'color: #CBCBCB;'
            """}
            QMenu::item:selected {"""
            f'background-color: #C8C8C8;'
            f'color: {color_black};'
            """}
            QMenu::item:pressed {"""
            f'background-color: #C8C8C8;'
            f'color: {color_black};'
            """}"""
        )
        self.mUi.mainwindow_menuHelp.setStyleSheet(
            """QMenu {"""
            f'background-color: #141822;'
            f'color: #CBCBCB;'
            """}
            QMenu::item:selected {"""
            f'background-color: #C8C8C8;'
            f'color: {color_black};'
            """}
            QMenu::item:pressed {"""
            f'background-color: #C8C8C8;'
            f'color: {color_black};'
            """}"""
        )
        # ----------------------------------------------------------------
        # Table widget CSS style. Dark.
        self.ttUi.tableW.setStyleSheet(
            """QTableWidget {"""
            f'background-color: {bgcol_transparent};'
            f'gridline-color: {color_5};'
            f'color: {color_name};'
            """}
            QTableView QTableCornerButton::section {"""
            f'background-color: {color_black};'
            """}
            QTableView QHeaderView::section {"""
            f'padding-left: auto;'
            f'padding-right: auto;'
            """}
            QHeaderView::section {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_name};'
            f'border: 2px solid {bgcol_transparent};'
            """}
            QHeaderView::section:checked {"""
            f'background-color: {color_disabled};'
            f'color: {color_white};'
            """}
            QHeaderView::section:selected {"""
            f'background-color: rgb(0, 85, 0);'
            f'color: {color_name};'
            f'border: 2px solid {bgcol_transparent};'
            """}
            QTableWidget::item {"""
            f'color: {color_name};'
            """}
            QTableWidget::item:selected {"""
            f'background-color: {color_disabled};'
            f'color: {color_white};'
            """}"""
        )
        # ----------------------------------------------------------------
        # Add event CSS style. Dark.
        self.aUi.setStyleSheet(
            f'background-color: rgba(34, 39, 51, 0.137);'
        )
        self.aUi.add_event_widget_form.setStyleSheet(
            f'background-color: {bgcol_distant};'
        )
        self.aUi.add_event_btn_add.setStyleSheet(
            """QPushButton {"""
            f'background-color: {color_default};'
            f'border-radius: 5px;'
            f'border: 2px solid  {color_default};'
            f'color: {color_white};'
            f'padding-top: 10 px;'
            f'padding-right: 23 px;'
            f'padding-left: 23 px;'
            f'padding-bottom: 10 px;'
            f'text-align: center;'
            f'margin-right: 8px;'
            """}
            QPushButton::hover {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_disabled};'
            f'border: 2px solid {color_theme};'
            """}"""
        )
        self.aUi.add_event_btn_cancel.setStyleSheet(
            """QPushButton {"""
            f'background-color: {bgcol_distant};'
            f'border-radius: 5px;'
            f'border: 2px solid {color_3};'
            f'color: {color_3};'
            f'padding-top: 10 px;'
            f'padding-right: 23 px;'
            f'padding-left: 23 px;'
            f'padding-bottom: 10 px;'
            f'text-align: center;'
            f'margin-left: 8px;'
            """}
            QPushButton::hover {"""
            f'background-color: {color_3};'
            f'color: {color_white};'
            f'border: 2px solid {color_3};'
            """}"""
        )
        self.aUi.add_event_comboBox_category.setStyleSheet(
            """QComboBox {"""
            f'font: 12pt;'
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_4};'
            f'border-radius: 5px;'
            f'color: {color_white};'
            """}
            QComboBox::hover {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_theme};'
            """}
            QComboBox QAbstractItemView {"""
            f'background-color: {bgcol_middle};'
            f'border: 2px solid  {color_hover_2};'
            f'color: #CBCBCB;'
            f'selection-background-color: {color_active};'
            f'selection-color: {color_black};'
            f'border-top-left-radius: 0;'
            f'border-top-right-radius: 0;'
            f'border-bottom-right-radius: 5px;'
            f'border-bottom-left-radius: 5px;'
            """}"""
        )
        self.aUi.add_event_dateEdit.setStyleSheet(
            """QDateEdit {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_4};'
            f'border-radius: 5px;'
            f'color: {color_white};'
            """}
            QDateEdit::hover {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_theme};'
            """}"""
        )
        self.aUi.add_event_lineEdit_name.setStyleSheet(
            """QLineEdit {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_4};'
            f'border-radius: 5px;'
            f'color: {color_white};'
            """}
            QLineEdit::hover {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_theme};'
            """}"""
        )
        self.aUi.add_event_lineEdit_time.setStyleSheet(
            """QLineEdit {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_4};'
            f'border-radius: 5px;'
            f'color: {color_white};'
            """}
            QLineEdit::hover {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_theme};'
            """}"""
        )
        self.aUi.add_event_plaintextedit_comment.setStyleSheet(
            """QPlainTextEdit {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_4};'
            f'border-radius: 5px;'
            f'color: {color_white};'
            """}
            QPlainTextEdit::hover {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_theme};'
            """}"""
        )
        self.aUi.add_event_textlbl_category.setStyleSheet(
            f'margin-top: 10px;'
            f'color: rgb(185, 185, 195);'
        )
        self.aUi.add_event_textlbl_comment.setStyleSheet(
            f'margin-top: 10px;'
            f'color: rgb(185, 185, 195);'
        )
        self.aUi.add_event_textlbl_date.setStyleSheet(
            f'margin-top: 10px;'
            f'color: rgb(185, 185, 195);'
        )
        self.aUi.add_event_textlbl_name.setStyleSheet(
            f'color: rgb(185, 185, 195);'
        )
        self.aUi.add_event_textlbl_time.setStyleSheet(
            f'margin-top: 10px;'
            f'color: rgb(185, 185, 195);'
        )
        self.aUi.add_event_widget_title_btn.setStyleSheet(
            f'background-color: {bgcol_middle};'
        )
        self.aUi.add_event_btn_exit.setStyleSheet(
            """QPushButton {"""
            f'color: {color_name};'
            f'background-color: {bgcol_transparent};'
            """}
            QPushButton::hover {"""
            f'color: {color_3};'
            """}"""
        )
        self.aUi.add_event_textlbl_title.setStyleSheet(
            f'color: {color_name};'
        )
        # ----------------------------------------------------------------
        # Edit event CSS style. Dark.
        self.eUi.setStyleSheet(
            f'background-color: rgba(34, 39, 51, 0.137);'
        )
        self.eUi.edit_event_widget_form.setStyleSheet(
            f'background-color: {bgcol_distant};'
        )
        self.eUi.edit_event_btn_save.setStyleSheet(
            """QPushButton {"""
            f'background-color: {color_default};'
            f'border-radius: 5px;'
            f'border: 2px solid  {color_default};'
            f'color: {color_white};'
            f'padding-top: 10 px;'
            f'padding-right: 23 px;'
            f'padding-left: 23 px;'
            f'padding-bottom: 10 px;'
            f'text-align: center;'
            f'margin-right: 8px;'
            """}
            QPushButton::hover {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_disabled};'
            f'border: 2px solid {color_theme};'
            """}"""
        )
        self.eUi.edit_event_btn_del.setStyleSheet(
            """QPushButton {"""
            f'background-color: {bgcol_distant};'
            f'border-radius: 5px;'
            f'border: 2px solid {color_3};'
            f'color: {color_3};'
            f'padding-top: 10 px;'
            f'padding-right: 23 px;'
            f'padding-left: 23 px;'
            f'padding-bottom: 10 px;'
            f'text-align: center;'
            f'margin-left: 8px;'
            """}
            QPushButton::hover {"""
            f'background-color: {color_3};'
            f'color: {color_white};'
            f'border: 2px solid {color_3};'
            """}"""
        )
        self.eUi.edit_event_comboBox_category.setStyleSheet(
            """QComboBox {"""
            f'font: 12pt;'
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_4};'
            f'border-radius: 5px;'
            f'color: {color_white};'
            """}
            QComboBox::hover {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_theme};'
            """}
            QComboBox QAbstractItemView {"""
            f'background-color: {bgcol_middle};'
            f'border: 2px solid  {color_hover_2};'
            f'color: #CBCBCB;'
            f'selection-background-color: {color_active};'
            f'selection-color: {color_black};'
            f'border-top-left-radius: 0;'
            f'border-top-right-radius: 0;'
            f'border-bottom-right-radius: 5px;'
            f'border-bottom-left-radius: 5px;'
            """}"""
        )
        self.eUi.edit_event_dateEdit.setStyleSheet(
            """QDateEdit {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_4};'
            f'border-radius: 5px;'
            f'color: {color_white};'
            """}
            QDateEdit::hover {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_theme};'
            """}"""
        )
        self.eUi.edit_event_lineEdit_name.setStyleSheet(
            """QLineEdit {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_4};'
            f'border-radius: 5px;'
            f'color: {color_white};'
            """}
            QLineEdit::hover {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_theme};'
            """}"""
        )
        self.eUi.edit_event_lineEdit_time.setStyleSheet(
            """QLineEdit {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_4};'
            f'border-radius: 5px;'
            f'color: {color_white};'
            """}
            QLineEdit::hover {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_theme};'
            """}"""
        )
        self.eUi.edit_event_plaintextedit_comment.setStyleSheet(
            """QPlainTextEdit {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_4};'
            f'border-radius: 5px;'
            f'color: {color_white};'
            """}
            QPlainTextEdit::hover {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_theme};'
            """}"""
        )
        self.eUi.edit_event_textlbl_category.setStyleSheet(
            f'margin-top: 10px;'
            f'color: rgb(185, 185, 195);'
        )
        self.eUi.edit_event_textlbl_comment.setStyleSheet(
            f'margin-top: 10px;'
            f'color: rgb(185, 185, 195);'
        )
        self.eUi.edit_event_textlbl_date.setStyleSheet(
            f'margin-top: 10px;'
            f'color: rgb(185, 185, 195);'
        )
        self.eUi.edit_event_textlbl_name.setStyleSheet(
            f'color: rgb(185, 185, 195);'
        )
        self.eUi.edit_event_textlbl_time.setStyleSheet(
            f'margin-top: 10px;'
            f'color: rgb(185, 185, 195);'
        )
        self.eUi.edit_event_widget_title_btn.setStyleSheet(
            f'background-color: {bgcol_middle};'
        )
        self.eUi.edit_event_btn_exit.setStyleSheet(
            """QPushButton {"""
            f'color: {color_name};'
            f'background-color: {bgcol_transparent};'
            """}
            QPushButton::hover {"""
            f'color: {color_3};'
            """}"""
        )
        self.eUi.edit_event_textlbl_title.setStyleSheet(
            f'color: {color_name};'
        )
        # ----------------------------------------------------------------
        # Category deleting CSS style. Dark.
        self.cUi.setStyleSheet(
            f'background-color: rgba(34, 39, 51, 0.137);'
        )
        self.cUi.category_delete_widget_form.setStyleSheet(
            f'background-color: {bgcol_distant};'
        )
        self.cUi.category_delete_btn_cancel.setStyleSheet(
            """QPushButton {"""
            f'background-color: {color_default};'
            f'border-radius: 5px;'
            f'border: 2px solid  {color_default};'
            f'color: {color_white};'
            f'padding-top: 10 px;'
            f'padding-right: 23 px;'
            f'padding-left: 23 px;'
            f'padding-bottom: 10 px;'
            f'text-align: center;'
            f'margin-right: 8px;'
            """}
            QPushButton::hover {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_disabled};'
            f'border: 2px solid {color_theme};'
            """}"""
        )
        self.cUi.category_delete_btn_delete.setStyleSheet(
            """QPushButton {"""
            f'background-color: {bgcol_distant};'
            f'border-radius: 5px;'
            f'border: 2px solid {color_3};'
            f'color: {color_3};'
            f'padding-top: 10 px;'
            f'padding-right: 23 px;'
            f'padding-left: 23 px;'
            f'padding-bottom: 10 px;'
            f'text-align: center;'
            f'margin-left: 8px;'
            """}
            QPushButton::hover {"""
            f'background-color: {color_3};'
            f'color: {color_white};'
            f'border: 2px solid {color_3};'
            """}"""
        )
        self.cUi.category_delete_comboBox_category.setStyleSheet(
            """QComboBox {"""
            f'font: 12pt;'
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_4};'
            f'border-radius: 5px;'
            f'color: {color_white};'
            """}
            QComboBox::hover {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_theme};'
            """}
            QComboBox QAbstractItemView {"""
            f'background-color: {bgcol_middle};'
            f'border: 2px solid  {color_hover_2};'
            f'color: rgb(203, 203, 203);'
            f'selection-background-color: rgb(94, 80, 238);'
            f'selection-color: rgb(0, 0, 0);'
            """}"""
        )
        self.cUi.category_delete_textlbl_category.setStyleSheet(
            f'margin-top: 10px;'
            f'color: rgb(185, 185, 195);'
        )
        self.cUi.category_delete_widget_title_btn.setStyleSheet(
            f'background-color: {bgcol_middle};'
        )
        self.cUi.category_delete_btn_exit.setStyleSheet(
            """QPushButton {"""
            f'color: {color_name};'
            f'background-color: {bgcol_transparent};'
            """}
            QPushButton::hover {"""
            f'color: {color_3};'
            """}"""
        )
        self.cUi.category_delete_textlbl_title.setStyleSheet(
            f'color: {color_name};'
        )

        # ----------------------------------------------------------------
        # Settings CSS style. Dark.
        self.sUi.setStyleSheet(
            f'background-color: {bgcol_distant};'
        )
        self.sUi.settings_btn_apply.setStyleSheet(
            """QPushButton {"""
            f'background-color: {color_default};'
            f'border-radius: 5px;'
            f'border: 2px solid  {color_default};'
            f'color: {color_white};'
            f'padding-top: 10 px;'
            f'padding-right: 23 px;'
            f'padding-left: 23 px;'
            f'padding-bottom: 10 px;'
            f'text-align: center;'
            f'margin-right: 5px;'
            """}
            QPushButton::hover {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_disabled};'
            f'border: 2px solid {color_theme};'
            """}"""
        )
        self.sUi.settings_btn_undo.setStyleSheet(
            """QPushButton {"""
            f'background-color: {bgcol_distant};'
            f'border-radius: 5px;'
            f'border: 2px solid {color_3};'
            f'color: {color_3};'
            f'padding-top: 10 px;'
            f'padding-right: 23 px;'
            f'padding-left: 23 px;'
            f'padding-bottom: 10 px;'
            f'text-align: center;'
            f'margin-left: 5px;'
            """}
            QPushButton::hover {"""
            f'background-color: {color_3};'
            f'color: {color_white};'
            f'border: 2px solid {color_3};'
            """}"""
        )
        self.sUi.settings_btn_export.setStyleSheet(
            """QPushButton {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_4};'
            f'border-radius: 5px;'
            f'color: {color_hover_1};'
            f'padding-top: 5 px;'
            f'padding-right: 23 px;'
            f'padding-left: 23 px;'
            f'padding-bottom: 5 px;'
            f'margin-right: 10px;'
            """}
            QPushButton::hover {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_disabled};'
            f'border: 1px solid {color_theme};'
            """}"""
        )
        self.sUi.settings_btn_import.setStyleSheet(
            """QPushButton {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_4};'
            f'border-radius: 5px;'
            f'color: {color_hover_1};'
            f'padding-top: 5 px;'
            f'padding-right: 23 px;'
            f'padding-left: 23 px;'
            f'padding-bottom: 5 px;'
            f'margin-right: 10px;'
            """}
            QPushButton::hover {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_disabled};'
            f'border: 1px solid {color_theme};'
            """}"""
        )
        self.sUi.settings_btn_telegram.setStyleSheet(
            """QPushButton {"""
            f'background-color: {bgcol_distant};'
            f'border: 1px solid {color_4};'
            f'border-radius: 5px;'
            f'color: {color_hover_1};'
            f'padding-left: 10px;'
            f'padding-right: 10px;'
            """}
            QPushButton::hover {"""
            f'background-color: {bgcol_distant};'
            f'color: {color_white};'
            f'border: 1px solid {color_theme};'
            """}"""
        )
        self.sUi.settings_imglbl_telegram_noverify.setStyleSheet(
            f'color: {color_3};'
        )
        self.sUi.settings_imglbl_telegram_verify.setStyleSheet(
            f'color: rgb(40, 199, 111);'
        )
        self.sUi.settings_lbl_error.setStyleSheet(
            f'font-size: 10pt;'
            f'color: {color_default};'
        )
        self.sUi.settings_lineedit_email.setStyleSheet(
            f'color:  {color_text};'
            f'background-color: {bgcol_distant};'
            f'border-radius: 5px;'
            f'text-decoration: underline;'
            f'font-size: 13pt;')
        self.sUi.settings_lineedit_email_new.setStyleSheet(
            """QLineEdit {"""
            f'color:  {color_text};'
            f'background-color: {bgcol_distant};'
            f'border: 1px solid  {color_border};'
            f'border-radius: 5px;'
            """}
            QLineEdit::hover {"""
            f'border: 1px solid {color_theme};'
            """}"""
        )
        self.sUi.settings_lineedit_newpass.setStyleSheet(
            """QLineEdit {"""
            f'color:  {color_text};'
            f'background-color: {bgcol_distant};'
            f'border: 1px solid  {color_border};'
            f'border-radius: 5px;'
            """}
            QLineEdit::hover {"""
            f'border: 1px solid {color_theme};'
            """}"""
        )
        self.sUi.settings_lineedit_oldpass.setStyleSheet(
            """QLineEdit {"""
            f'color:  {color_text};'
            f'background-color: {bgcol_distant};'
            f'border: 1px solid  {color_border};'
            f'border-radius: 5px;'
            """}
            QLineEdit::hover {"""
            f'border: 1px solid {color_theme};'
            """}"""
        )
        self.sUi.settings_lineedit_repnewpass.setStyleSheet(
            """QLineEdit {"""
            f'color:  {color_text};'
            f'background-color: {bgcol_distant};'
            f'border: 1px solid  {color_border};'
            f'border-radius: 5px;'
            """}
            QLineEdit::hover {"""
            f'border: 1px solid {color_theme};'
            """}"""
        )
        self.sUi.settings_text_edit_info.setStyleSheet(
            f'color: {color_white};'
        )
        self.sUi.settings_text_email.setStyleSheet(
            f'color: {color_hover_1};'
        )
        self.sUi.settings_text_email_2.setStyleSheet(
            f'color: {color_hover_1};'
        )
        self.sUi.settings_text_internet.setStyleSheet(
            f'color: {color_hover_1};'
        )
        self.sUi.settings_text_newpass.setStyleSheet(
            f'color: {color_hover_1};'
        )
        self.sUi.settings_text_oldpass.setStyleSheet(
            f'color: {color_hover_1};'
        )
        self.sUi.settings_text_repnewpass.setStyleSheet(
            f'color: {color_hover_1};'
        )

        # ----------------------------------------------------------------
        # About us CSS style. Dark.
        self.abUi.setStyleSheet(
            f'background-color: {bgcol_middle};'
        )
        self.abUi.about_us_btn_exit.setStyleSheet(
            """QPushButton {"""
            f'color: {color_name};'
            f'background-color: {bgcol_transparent};'
            """}
            QPushButton::hover {"""
            f'color: {color_3};'
            """}"""
        )
        self.abUi.about_us_imglabel_alex.setStyleSheet(
            """QLabel {"""
            f'background-image: url(design/img/team/team_02.jpg);'
            f'{about_us_border};'
            """}"""
        )
        self.abUi.about_us_imglabel_dimon.setStyleSheet(
            """QLabel {"""
            f'background-image: url(design/img/team/team_04.jpg);'
            f'{about_us_border};'
            """}"""
        )
        self.abUi.about_us_imglabel_kolesnikov.setStyleSheet(
            """QLabel {"""
            f'background-image: url(design/img/team/team_07.jpg);'
            f'{about_us_border};'
            """}"""
        )
        self.abUi.about_us_imglabel_oleg.setStyleSheet(
            """QLabel {"""
            f'background-image: url(design/img/team/team_05.jpg);'
            f'{about_us_border};'
            """}"""
        )
        self.abUi.about_us_imglabel_simonovsky.setStyleSheet(
            """QLabel {"""
            f'background-image: url(design/img/team/team_08.jpg);'
            f'{about_us_border};'
            """}"""
        )
        self.abUi.about_us_imglabel_timofey.setStyleSheet(
            """QLabel {"""
            f'background-image: url(design/img/team/team_01.jpg);'
            f'{about_us_border};'
            """}"""
        )
        self.abUi.about_us_imglabel_vlad.setStyleSheet(
            """QLabel {"""
            f'background-image: url(design/img/team/team_06.jpg);'
            f'{about_us_border};'
            """}"""
        )
        self.abUi.about_us_imglabel_yuri.setStyleSheet(
            """QLabel {"""
            f'background-image: url(design/img/team/team_03.jpg);'
            f'{about_us_border};'
            """}"""
        )
        self.abUi.about_us_textlabel_about_program.setStyleSheet(
            f'color: {color_name};'
        )
        self.abUi.about_us_textlabel_alex.setStyleSheet(
            f'color: {color_name};'
        )
        self.abUi.about_us_textlabel_copyright.setStyleSheet(
            f'color: {color_name};'
        )
        self.abUi.about_us_textlabel_dimon.setStyleSheet(
            f'color: {color_name};'
        )
        self.abUi.about_us_textlabel_kolesnikov.setStyleSheet(
            f'color: {color_name};'
        )
        self.abUi.about_us_textlabel_oleg.setStyleSheet(
            f'color: {color_name};'
        )
        self.abUi.about_us_textlabel_simonovsky.setStyleSheet(
            f'color: {color_name};'
        )
        self.abUi.about_us_textlabel_team_left.setStyleSheet(
            f'color: {color_name};'
        )
        self.abUi.about_us_textlabel_team_right.setStyleSheet(
            f'color: {color_name};'
        )
        self.abUi.about_us_textlabel_timofey.setStyleSheet(
            f'color: {color_name};'
        )
        self.abUi.about_us_textlabel_version.setStyleSheet(
            f'color: {color_name};'
        )
        self.abUi.about_us_textlabel_vlad.setStyleSheet(
            f'color: {color_name};'
        )
        self.abUi.about_us_textlabel_yuri.setStyleSheet(
            f'color: {color_name};'
        )

        self.status = True

    def white_theme(self):
        # ----------------------------------------------------------------
        # Login CSS style. Light.
        self.lUi.setStyleSheet(
            f'background-color: #F8F8F8;'
        )

        # ----------------------------------------------------------------
        # Register CSS style. Light.
        self.rUi.setStyleSheet(
            f'background-color: #F8F8F8;'
        )

        # ----------------------------------------------------------------
        # Main UI. Light.
        self.mUi.setStyleSheet(
            f'background-color: #F8F8F8;'
        )

        # ----------------------------------------------------------------
        # Table widget CSS style. Light.
        self.ttUi.setStyleSheet(
            f'background-color: #F8F8F8;'
        )

        # ----------------------------------------------------------------
        # Add event CSS style. Light.
        self.aUi.setStyleSheet(
            f'background-color: #F8F8F8;'
        )

        # ----------------------------------------------------------------
        # Edit event CSS style. Light.
        self.eUi.setStyleSheet(
            f'background-color: #F8F8F8;'
        )

        # ----------------------------------------------------------------
        # Category deleting CSS style. Light.
        self.cUi.setStyleSheet(
            f'background-color: #F8F8F8;'
        )

        # ----------------------------------------------------------------
        # Settings CSS style. Light.
        self.sUi.setStyleSheet(
            f'background-color: #F8F8F8;'
        )

        # ----------------------------------------------------------------
        # About us CSS style. Light.
        self.abUi.setStyleSheet(
            f'background-color: #F8F8F8;'
        )

        self.status = False


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainUI()
    sys.exit(app.exec())

    # dbl = DbLogic()
    # dbl.set_logged_user_data(user_login='Ева', item='set_working_user')
    # dbl.get_logged_user_data(user_login='Ева', item='set_working_user')

    # print(dbl.set_logged_user_data(
    #     item='import_add', edit_params=['1', '2', '3', '4']))
