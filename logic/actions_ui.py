import datetime
import sys
sys.path.append('.')

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate

from logic.dblogic import DbLogic as db


class ActionsUI(QtWidgets.QMainWindow):
    '''
    This class implements adding and editing actions.
    '''

    def __init__(self, user):
        super().__init__()
        # Creating database instance.
        self.timedb = db

        # Getting current user name.
        self.user_n_name = user

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
        

    def ui_add_event_preparations(self):
        # Settings for 'a_dE_date' control element.
        self.aUi.add_event_dateEdit.setCalendarPopup(True)
        self.aUi.add_event_dateEdit.setDate(QDate(QDate.currentDate()))
        self.aUi.add_event_dateEdit.setMaximumDate(QDate(QDate.currentDate()))

        categs = self.timedb().get_user_categories(self.user_n_name)
        i = 0
        for categ in categs:
            self.aUi.add_event_comboBox_category.insertItem(i, categ)
            i += 1

    def ui_edit_event_preparations(self, settings):
        self.eUi.edit_event_dateEdit.setCalendarPopup(True)
        self.eUi.edit_event_dateEdit.setMaximumDate(QDate(QDate.currentDate()))

        categs = self.timedb().get_user_categories(self.user_n_name)
        i = 0
        for categ in categs:
            self.aUi.edit_event_comboBox_category.insertItem(i, categ)
            i += 1

        current_date = settings[2]

        self.eUi.edit_event_lineEdit_name.text(settings[0])
        self.eUi.edit_event_comboBox_category.itemText(0, settings[3])
        self.eUi.edit_event_lineEdit_time.text(settings[1])
        # self.eUi.edit_event_dateEdit.setDate()
        self.eUi.edit_event_plaintextedit_comment.setPlainText(settings[4])

    def show_add_event(self):
        self.ui_add_event_preparations()
        self.aUi.show()

    def show_edit_event(self, actl_name, act_time, act_date, cat_name, act_comment):
        settings = [actl_name, actl_name, act_time, act_date, cat_name, act_comment]
        self.ui_edit_event_preparations(settings)
        self.eUi.show()

    def add_event(self):
        # Getting all info, entered by user.
        title = self.aUi.add_event_lineEdit_name.text()        
        category = self.aUi.add_event_comboBox_category.currentText()
        duration = self.aUi.add_event_lineEdit_time.text()
        date = self.aUi.add_event_dateEdit.date()
        comment = self.aUi.add_event_plaintextedit_comment.toPlainText()

        date_ = datetime.date(date.year(), date.month(), date.day())
        str_date = date_.strftime('%Y-%m-%d')
        
        int_duration = int(''.join(filter(str.isdigit, duration)))

        # Writing all changes to db and closing 'Add Event' win.
        self.timedb().add_event(self.user_n_name, title, int_duration, str_date,\
            category, comment)
        self.aUi.close()

    def suppose_category(self):
        pass

    def edit_event(self):
        pass
        


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = ActionsUI()
    sys.exit(app.exec())
