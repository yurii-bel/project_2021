import sys
import uuid
import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTime, QDate
from PyQt5 import QtCore, QtGui, QtWidgets

from logic.addding_editing_actions import Actions
from testing.actions_ui_test.edit import Ui_Form


class ActionUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.aUi = Ui_Form()
        self.aUi.setupUi(self)
        self.userId = str(uuid.uuid4())
        self.user_events = {}
        self.categs = ['Отдых', 'Спорт', 'Семья', 'Работа', 'Учёба']

        # Connecting buttons.
        self.aUi.btn_save.clicked.connect(self.add_event)
        self.aUi.btn_edit.clicked.connect(self.edit_event)

        self.act = Actions

    def add_event(self):
        # Settings for 'dE_date' control element.
        self.aUi.dE_date.setCalendarPopup(True)
        self.aUi.dE_date.setDate(QDate(QDate.currentDate()))
        self.aUi.dE_date.setMaximumDate(QDate(QDate.currentDate()))

        # Settings for 'tE_time' control element.
        self.aUi.tE_time.setTime(QTime.currentTime())

        # Settings for cB_category control element.
        self.aUi.cB_category.addItems(self.categs)

        title = self.aUi.lE_name.text()
        category = self.aUi.cB_category.currentText()
        
        time = self.aUi.tE_time.time()
        hour = time.hour()
        minute = time.minute()

        date = self.aUi.dE_date.date()
        year = date.year()
        month = date.month()
        day = date.day()

        duration = self.aUi.lE_duration.text()        
        comment = self.aUi.tE_comment.toPlainText()

        self.added_event = self.act(title, category, hour, minute, year, \
            month, day, duration, comment)
        self.added_event.categories = self.categs

        self.json_event = {'UserID':self.userId, 
        'EventDetails':{
            'title':self.added_event.action,
            'category':self.added_event.category,
            'time':[
                self.added_event.hour, self.added_event.minute,
            ],
            'date':[
                self.added_event.year, self.added_event.month, \
                    self.added_event.day,
            ],
            'duration':self.added_event.duration,
            'comment':self.added_event.comment
        }}

        self.user_events.update(self.json_event)

        self.aUi.cB_category.addItems(self.added_event.categories)
        self.aUi.tE_comment.setPlainText(f'{[*self.user_events.values()]}')

    def edit_event(self):
        # Settings for 'lE_name' control element.
        self.aUi.lE_name.setText(self.added_event.action)

        # Settings for cB_category control element.
        self.aUi.cB_category.setCurrentText(self.added_event.category)
        self.aUi.cB_category.addItems(self.categs)

        # Settings for 'dE_date' input element.
        self.aUi.dE_date.setCalendarPopup(True)
        edit_date = QDate(int(self.added_event.year), \
            int(self.added_event.month), int(self.added_event.day))
        self.aUi.dE_date.setDate(edit_date)
        self.aUi.dE_date.setMaximumDate(QDate(QDate.currentDate()))

        # Settings for 'tE_time' input element.
        edit_time = QTime(int(self.added_event.hour), \
            int(self.added_event.minute))
        self.aUi.tE_time.setTime(edit_time)

        # Settings for 'lE_duration' input element.
        self.aUi.lE_duration.setText(self.added_event.duration)

        # Settings for 'lE_duration' input element.
        self.aUi.tE_comment.setPlainText(self.added_event.comment)

        title = self.aUi.lE_name.text()
        category = self.aUi.cB_category.currentText()
        
        time = self.aUi.tE_time.time()
        hour = time.hour()
        minute = time.minute()

        date = self.aUi.dE_date.date()
        year = date.year()
        month = date.month()
        day = date.day()

        duration = self.aUi.lE_duration.text()        
        comment = self.aUi.tE_comment.toPlainText()

        self.added_event = self.act(title, category, hour, minute, year, \
            month, day, duration, comment)

        json_event = {'UserID':self.userId, 
        'EventDetails':{
            'title':self.added_event.action,
            'category':self.added_event.category,
            'time':[
                self.added_event.hour, self.added_event.minute,
            ],
            'date':[
                self.added_event.year, self.added_event.month, \
                    self.added_event.day,
            ],
            'duration':self.added_event.duration,
            'comment':self.added_event.comment
        }}
        self.json_event.update(json_event)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = ActionUI()
    win.show()
    sys.exit(app.exec())
    