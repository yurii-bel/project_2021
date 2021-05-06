import datetime
import json
import sys
import os
from PyQt5 import QtGui, QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit, QLabel, QComboBox


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


class MainWindow(QtWidgets.QWidget):
    """
    This class implements the user interface for program logic.
    """
    def __init__(self, parent=None):
        super().__init__()
        self.categories = ['Sport', 'Chill', 'Family']
        
        self.actions_block()
        self.date_search_block()
        
        #self.btn_save.clicked.connect(self...)
        
        self.initUI()
        
        """
        self.ui = uic.loadUi("test_ui.ui")

        self.current_date = datetime.datetime.now()
        self.main_class = Action

        self.ui.comboBox.addItems(self.categories)
        self.ui.btn_save.clicked.connect(self.get_values)

        self.ui.dateEdit.setDate(self.current_date)

        self.ui.show()
        """
    
    # def get_values(self):
    #     time = self.ui.timeEdit.time().toString()
    #     date = self.ui.dateEdit.date().toString()
    #     category = self.ui.comboBox.currentText()

    #     shit = self.main_class('run', category, time, date, 'ass') # shit contains a reference to class Action with args.

    #     self.ui.main_label.setWordWrap(True)
    #     self.ui.main_label.setText(shit.__str__())

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle('TimeSoft')
        
        self.show()

    def actions_block(self):
        self.categories = ['Sport', 'Chill', 'Family', 'Other']  # Categories for comboBox.

        self.lbl_action = QLabel('Add action:') # Labels for user input block.
        self.lbl_comments = QLabel('Comments:')
        self.lbl_date = QLabel('Date:')
        self.lbl_duration = QLabel('Duration:')
        self.lbl_category = QLabel('Category:')

        self.lbl_action.move(510, 80) # Moving labels to the right locations.
        self.lbl_category.move(510, 120)
        self.lbl_duration.move(510, 160)
        self.lbl_date.move(510, 200)
        self.lbl_comments.move(510, 240)


        self.qLe_add_action = QLineEdit(self) # Adding input types
        self.qLe_add_action.move(570,80) # for corresponding labels.
        self.qLe_add_action.resize(191,20)

        self.cBox_category = QComboBox(self)
        self.cBox_category.addItems(self.categories)
        self.cBox_category.setEditable(True)

        self.cBox_category.move(570, 120)
        # self.cBox_category.clicked.connect(self.get_values)


        self.btn_save = QPushButton('Save', self)
        self.btn_save.setObjectName('btn')
        self.btn_save.setToolTip('This is a button')
        self.btn_save.setStyleSheet('QPushButton {background-color: #4B0082; color: #fff;}')
        self.btn_save.move(570, 340)
        

    def updateCategList(self):
        pass
        # it will be used in future (or not D:). 
        # if self.cBox_category.currentText() not in self.categories:
        #     self.categories.append(self.cBox_category.currentText()) 
        #     self.cBox_category.addItem(self.cBox_category.currentText())

    
    def visualization_block(self):
        self.btn_table = QPushButton("Table", self)
        self.btn_graph = QPushButton("Graph", self)
        self.btn_diagram = QPushButton("Diagram", self)

        self.btn_table.move(30, 100)
        self.btn_graph.move(30, 140)
        self.btn_diagram.move(30, 180)

    def date_search_block(self):
        self.lbl_date = QLabel("Enter date: ", self)
        self.lbl_date_addaction = QLineEdit(self)
        self.btn_show = QPushButton("Show", self)

        self.lbl_date.move(190, 80)
        self.lbl_date_addaction.move(250, 80)
        self.lbl_category.resize(113, 20)
        self.btn_show.move(370, 80)




if __name__ == '__main__':
    action, category, time, date, comment = 'run', 'sport', '22:13:59', '05/05/2021', 'some shit'
    # print(Action(action, category, time, date, comment))
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())