import datetime
import json
import sys
import os
from PyQt5 import QtGui, QtWidgets, QtCore, uic


class Action:
    """
    This class describes actions logic.
    """
    def __init__(self, action=None, category=None, time=None, date=None, comment=None):
        self.action = action
        self.category = category
        self.time = time
        self.date = date
        self.comment = comment

        self.check_input_data()

    def check_input_data(self):
        if not isinstance(self.action, str):
            pass

        if not isinstance(self.comment, str):
            pass

    def save_action(self):  # Save current action
        pass

    def edit_action(self):  # Edit chosen action
        pass

    def delete_action(self):  # Delete chosen action
        pass

    def __str__(self):
        return f'\naction: {self.action}' \
               f'\ncategory: {self.category}' \
               f'\ntime: {self.time}' \
               f'\ndate: {self.date}' \
               f'\ncomment {self.comment}'


class Database:
    """
    This class operates with SQL database.
    """
    def __init__(self):
        pass

    def send_to(self):
        """
        This method sends data to sql database.
        """
        pass

    def get_from(self):
        """
        This method gets data from sql database.
        """
        pass

    def change_data(self):
        """
        This method changes any data in sql Database.
        """
        pass


class Diagram:
    """
    This method helps to build and show various diagrams and plots.
    """
    def __init__(self):
        pass

    def build_plot(self):
        """
        This method builds a plot for user data.
        """
        pass

    def build_table(self):
        """
        This method builds a table for user data.
        """
        pass

    def build_diagram(self):
        """
        This method builds a diagram for user data.
        """
        pass

    def show_plot(self):
        """
        This method shows a plot in UI.
        """
        pass

    def show_table(self):
        """
        This method shows a table in UI.
        """
        pass

    def show_diagram(self):
        """
        This method shows a diagram in UI.
        """
        pass


class ImportExport:
    """
    This class implements import\export features.
    """
    def __init__(self):
        pass

    def import_csv(self):
        """
        This method imports data to a program from an existing .csv file.
        """
        pass

    def export_csv(self):
        """
        This method exports data from a program to a new .csv file.
        """
        pass

    def import_user_settings(self):
        """
        This method imports user settings from an existing .json file.
        """ 
        pass

    def export_user_settings(self):
        """
        This method exports user settings to a new .json file.
        """ 
        pass


class DataForecast:
    """
    This class operates with various modules, such as pandas and seaborn, and
    forecasts the data, using categories and date interval.
    https://duchesnay.github.io/pystatsml/statistics/time_series.html?highlight=forecast
    """
    def __init__(self):
        pass


class MainWindow(QtWidgets.QMainWindow):
    """
    This class implements the user interface for program logic.
    """
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.categories = ['Sport', 'Chill', 'Family']
        self.ui = uic.loadUi("test_ui.ui")

        self.current_date = datetime.datetime.now()
        self.main_class = Action

        self.ui.comboBox.addItems(self.categories)
        self.ui.btn_save.clicked.connect(self.get_values)

        self.ui.dateEdit.setDate(self.current_date)

        self.ui.show()

    def get_values(self):
        time = self.ui.timeEdit.time().toString()
        date = self.ui.dateEdit.date().toString()
        category = self.ui.comboBox.currentText()

        shit = self.main_class('run', category, time, date, 'ass') # shit contains a reference to class Action with args.

        self.ui.main_label.setWordWrap(True)
        self.ui.main_label.setText(shit.__str__())


if __name__ == '__main__':
    action, category, time, date, comment = 'run', 'sport', '22:13:59', '05/05/2021', 'some shit'
    # print(Action(action, category, time, date, comment))
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())