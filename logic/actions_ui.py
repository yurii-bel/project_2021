import time
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate

sys.path.append('.')

from logic.dblogic import DbLogic as db
from logic.actions import Actions
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import timeSoft


class ActionsUI(QtWidgets.QMainWindow):
    '''
    This class implements adding and editing actions.
    '''

    def __init__(self):
        super().__init__()
        # Creating database instance.
        self.timedb = db

        # Getting current user name.
        # self.user_n_name = timeSoft.MainUI().get_user_n_name()

        # Instance of main logic.
        self.act = Actions

        # Loading appropriate UI's.
        self.aUi = uic.loadUi('design\\add_event_d.ui')
        self.eUi = uic.loadUi('design\\edit_event_d.ui')

        # Connecting buttons to appropriate slots.
        self.aUi.add_event_btn_add.clicked.connect(self.add_event)
        self.aUi.add_event_btn_cancel.clicked.connect(self.aUi.close)
        self.aUi.add_event_btn_exit.clicked.connect(self.aUi.close)

        # Connecting line edits to appropriate slots.
        self.aUi.add_event_lineEdit_name.textChanged.connect(
            self.suppose_category)

        # Settings and preparations for many control elements.
        self.ui_preparations()

    def ui_preparations(self):
        # For time of event cration in add_event_btn_add.
        time_ = time.localtime()
        self._time = time.strftime('%X', time_)

        # Settings for 'a_dE_date' control element.
        self.aUi.add_event_dateEdit.setCalendarPopup(True)
        self.aUi.add_event_dateEdit.setDate(QDate(QDate.currentDate()))
        self.aUi.add_event_dateEdit.setMaximumDate(QDate(QDate.currentDate()))

        # categs = self.timedb().get_user_categories(self.user_n_name)
        # for categ in categs:
        #     self.aUi.add_event_comboBox_category.setItems(categ)

    def show_add_event(self):
        self.aUi.show()

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
        self.added_event = self.act(title, category, hour, minute, second,
                                    year, month, day, duration, comment)

        # Using test database!
        # # Writing all changes to db and closing 'Add Event' win.
        self.db.set_data('1', '43', self.added_event.action,
                         self.added_event.category, self.added_event.duration,
                         self.added_event.time, self.added_event.date,
                         self.added_event.comment, 'Activity')
        self.aUi.close()

    def suppose_category(self):
        pass

    def edit_event(self):
        # This method is reserved for future editing actions.
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = ActionsUI()
    sys.exit(app.exec())
