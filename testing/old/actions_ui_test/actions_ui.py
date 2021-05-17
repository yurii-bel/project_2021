import sys
import uuid
import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTime, QDate
from PyQt5 import QtCore, QtGui, QtWidgets

#from actions import Actions
#from ..design.edit_event import Ui_Form

sys.path.append(os.getcwd())


class ActionUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # self.aUi = uic.loadUi('design\\edit_event.ui')
        self.aUi = Ui_Form()
        self.aUi.setupUi(self)
        self.user_events = {}   

        # Settings for 'dE_date' control element.
        self.aUi.dE_date.setCalendarPopup(True)
        self.aUi.dE_date.setDate(QDate(QDate.currentDate()))
        self.aUi.dE_date.setMaximumDate(QDate(QDate.currentDate()))

        # Settings for 'tE_time' control element.
        self.aUi.tE_time.setTime(QTime.currentTime())

        # Settings for cB_category control element.
        # self.aUi.cB_category.addItems()

        self.aUi.btn_save.clicked.connect(self.add_event)

        self.act = Actions

    def add_event(self):
        userId = uuid.uuid4()

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

        a = self.act(title, category, hour, minute, year, month, day, \
            duration, comment)
        b = {userId:a.__str__()}

        self.user_events.update(b)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = ActionUI()
    win.show()
    sys.exit(app.exec())
    