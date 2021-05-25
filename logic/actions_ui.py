import datetime
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate

sys.path.append('.')

from logic.dblogic import DbLogic as db
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
        # Settings for 'a_dE_date' control element.
        self.aUi.add_event_dateEdit.setCalendarPopup(True)
        self.aUi.add_event_dateEdit.setDate(QDate(QDate.currentDate()))
        self.aUi.add_event_dateEdit.setMaximumDate(QDate(QDate.currentDate()))

        categs = self.timedb().get_user_categories('Sif')
        i = 0
        for categ in categs:
            self.aUi.add_event_comboBox_category.insertItem(i, categ)
            i += 1

        # self.show_add_event()

    def show_add_event(self):
        self.aUi.show()

    def add_event(self):
        # Getting all info, entered by user.
        title = self.aUi.add_event_lineEdit_name.text()        
        category = self.aUi.add_event_comboBox_category.currentText()
        duration = self.aUi.add_event_lineEdit_time.text()
        date = self.aUi.add_event_dateEdit.date()
        comment = self.aUi.add_event_plaintextedit_comment.toPlainText()

        date_ = datetime.date(date.year(), date.month(), date.day())
        str_date = date_.strftime('%Y-%m-%d')
        
        # if 'м' or 'm' in duration:
        #     duration = int(duration)

        # Writing all changes to db and closing 'Add Event' win.
        self.timedb().add_event('Timofey', title, duration, str_date,\
            category, comment)
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
