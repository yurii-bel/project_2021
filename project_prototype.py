import datetime
import json
import sys
import os
from PyQt5 import QtGui, QtWidgets, QtCore, uic


class MainApp:
    """
    Description of class MainApp
    """
    def __init__(self, action=None, category=None, time=None, date=None, comment=None):
        self.action = action
        self.category = category
        self.time = time
        self.date = date
        self.comment = comment

        self.current_date = datetime.datetime.now()
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

    def plot_diagram(self):  # Plot diagram (use csv file)
        pass

    def change_language(self):  # Change language of UI
        pass

    def change_theme(self):  # Change UI theme
        pass

    def change_diagram_type(self):  # Change type of a diagram
        pass

    def __str__(self):
        return f'\naction: {self.action}' \
               f'\ncategory: {self.category}' \
               f'\ntime: {self.time}' \
               f'\ndate: {self.date}' \
               f'\ncomment {self.comment}'


class SearchField:
    """
    Description of class SearchField
    """
    def __init__(self):
        self.activity = None
        self.duration = None
        self.date = None
        self.tasks = None
        self.counter = 0
        self.inp = input('Enter activity, duration and date: ')

        self.get_input()
        self.save_to_txt()

    def get_input(self):
        l_inp = list(self.inp)
        task = ''.join(l_inp).split()
        self.activity = task[0]
        self.duration = task[1]
        self.date = task[2]
        self.tasks = {f'{self.counter}': task}

        self.counter += 1

    def save_to_txt(self):
        with open('data.txt', 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)

    # def update_json(self):
    #     with open("data.txt", "r+") as file:
    #         data = json.load(file)
    #         data.update(self.tasks)
    #         file.seek(0)
    #         json.dump(data, file)

    def __str__(self):
        return f'\nactivity: {self.activity}' \
               f'\nduration: {self.duration}' \
               f'\ndate: {self.date}' \
               f'\ntask: {self.tasks}'


class MainWindow(QtWidgets.QMainWindow):
    """
    Description of class MainWindow
    """

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.categories = ['Sport', 'Chill', 'Family']
        self.ui = uic.loadUi("test_ui.ui")

        self.main_class = MainApp

        self.ui.comboBox.addItems(self.categories)
        self.ui.btn_save.clicked.connect(self.get_values)

        self.ui.show()

    def get_values(self):
        time = self.ui.timeEdit.time()
        date = self.ui.dateEdit.date()
        category = self.ui.comboBox.currentText()

        shit = self.main_class('run', category, time, date, 'ass')

        self.ui.main_label.setWordWrap(True)
        self.ui.main_label.setText(self.main_class().__str__())


if __name__ == '__main__':
    action, category, time, date, comment = 'run', 'sport', '22:13:59', '05/05/2021', 'some shit'
    print(MainApp(action, category, time, date, comment))
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

    # # datetime object containing current date and time
    # now = datetime.datetime.now()
    #
    # print("now =", now)
    #
    # # dd/mm/YY H:M:S
    # dt_date = now.strftime('%d/%m/%Y')
    # dt_time = now.strftime('%H:%M:%S')
    # dt_h = now.strftime('%H')
    # print('date: ', dt_date)
    # print('time: ', dt_time)
    # print('Hours: ', dt_h)
