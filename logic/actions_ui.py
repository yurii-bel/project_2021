import sys
sys.path.append('.')
import sqlite3
import time

from PyQt5.QtCore import QDate
from PyQt5 import QtWidgets, uic

from logic.actions import Actions


class ActionsUI(QtWidgets.QMainWindow):
    '''
    This class implements adding and editing actions.
    '''
    def __init__(self):
        super().__init__()

        # Loading appropriate UI's.
        self.aUi = uic.loadUi('design\\add_event.ui')
        self.eUi = uic.loadUi('design\\edit_event.ui')

        # For time of event cration in a_save_event.
        time_ = time.localtime()
        self._time = time.strftime('%X', time_)

        # Connecting to db.
        self.db = sqlite3.connect('database\\timo364\\TimeSoft.db')
        self.curs = self.db.cursor()

        # Categories for 'a_cB_category' control element.
        self.categs = ['Здоровье', 'Работа', 'Семья', 'Отдых', 'Развлечения', \
            'Другое']

        # Settings for 'a_dE_date' control element.
        self.aUi.a_dateEdit.setCalendarPopup(True)
        self.aUi.a_dateEdit.setDate(QDate(QDate.currentDate()))
        self.aUi.a_dateEdit.setMaximumDate(QDate(QDate.currentDate()))

        # Settings for 'a_cB_category' control element.
        self.aUi.a_comboBox.addItems(self.categs)

        self.aUi.a_btn_save.clicked.connect(self.add_event)
        self.aUi.a_btn_del.clicked.connect(self.aUi.close)
        self.aUi.a_btn_exit.clicked.connect(self.aUi.close)

        # Instance of main logic.
        self.act = Actions

    def add_event(self):
        # Getting all info, entered by user. 
        title = self.aUi.a_lineEdit_name.text()
        category = self.aUi.a_comboBox.currentText()

        hour_ = int(self._time[:2])  # getting hours from time.localtime()
        minute_ = int(self._time[3:5])  # getting minutes from time.localtime()
        second_ = int(self._time[6:9])  # getting seconds from time.localtime()
        hour = hour_
        minute = minute_
        second = second_
        
        date = self.aUi.a_dateEdit.date()
        year = date.year()
        month = date.month()
        day = date.day()
        
        duration = self.aUi.a_lineEdit_time.text()        
        comment = self.aUi.a_te_comment.toPlainText()

        # Using main logic and writing all recieved info.
        self.added_event = self.act(title, category, hour, minute, second, \
            year, month, day, duration, comment)

        # Using test database!
        # Writing created event to db.
        data = (self.added_event.action, \
            self.added_event.category, self.added_event.duration, \
                self.added_event.time, self.added_event.date, \
                    self.added_event.comment)
        self.curs.execute('insert into Actions values(?,?,?,?,?,?)', \
            data)       

        # Writing all changes to db and closing 'Add Event' win.
        self.db.commit()
        self.aUi.close()

    def edit_event(self):
        # This method is reserved for future editing actions.
        pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = ActionsUI()
    sys.exit(app.exec())
    