import sys
sys.path.append('.')
import sqlite3
import time

from PyQt5.QtCore import QDate
from PyQt5 import QtWidgets, uic

from logic.addding_editing_actions import Actions


class ActionUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.aUi = uic.loadUi('design\\add_event.ui')
        self.eUi = uic.loadUi('design\\edit_event.ui')

        # This method of showing ui is broken.
        # self.eUi = EditUI()
        # self.eUi.setupUi(self)

        # For time of event cration in a_save_event.
        time_ = time.localtime()
        self._time = time.strftime('%X', time_)

        # Connecting to db.
        self.db = sqlite3.connect('database\\timo364\\TimeSoft.db')
        self.curs = self.db.cursor()

        # Categories for cB_category control element.
        self.categs = ['Здоровье', 'Работа', 'Семья', 'Отдых', 'Развлечения', \
            'Другое']

        # Settings for 'dE_date' control element.
        self.aUi.dE_date.setCalendarPopup(True)
        self.aUi.dE_date.setDate(QDate(QDate.currentDate()))
        self.aUi.dE_date.setMaximumDate(QDate(QDate.currentDate()))

        # Settings for cB_category control element.
        self.aUi.cB_category.addItems(self.categs)

        self.aUi.btn_save.clicked.connect(self.add_event)
        self.aUi.btn_cancel.clicked.connect(self.aUi.close)

        self.act = Actions

    def add_event(self):
        title = self.aUi.lE_name.text()
        category = self.aUi.cB_category.currentText()

        hour_ = int(self._time[:2])
        minute_ = int(self._time[3:5])
        second_ = int(self._time[6:9])
        hour = hour_
        minute = minute_
        second = second_
        
        date = self.aUi.dE_date.date()
        year = date.year()
        month = date.month()
        day = date.day()
        
        duration = self.aUi.lE_duration.text()        
        comment = self.aUi.tE_comment.toPlainText()

        self.added_event = self.act(title, category, hour, minute, second, \
            year, month, day, duration, comment)

        # Writing created event to db.
        data = (self.added_event.action, \
            self.added_event.category, self.added_event.duration, \
                self.added_event.time, self.added_event.date, \
                    self.added_event.comment)
        self.curs.execute('insert into Actions values(?,?,?,?,?,?)', \
            data)       

        self.db.commit()
        self.aUi.close()

    def close_add_event(self):
        self.aUi.close()

    def edit_event(self):
        pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = ActionUI()
    sys.exit(app.exec())
    