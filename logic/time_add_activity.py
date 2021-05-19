import sys
sys.path.append('.')
import sqlite3
from datetime import datetime

from logic.time_db import TimeDb
from logic.actions_ui import ActionsUI
from PyQt5.QtCore import QDate
from PyQt5 import QtWidgets, uic

class ActionsUI(QtWidgets.QMainWindow):
    '''
    This class implements adding and editing actions.
    '''
    def __init__(self):
        super().__init__()

        # Loading class for db operations.
        self.timedb = TimeDb

        # Loading appropriate UI's.
        self.addEventUi = uic.loadUi('design\\add_event.ui')
        self.editEventUi = uic.loadUi('design\\edit_event.ui')
        
        self.addEventUi.show()
        # Categories for 'a_cB_category' control element.
        self.categs = ['Здоровье', 'Работа', 'Семья', 'Отдых', 'Развлечения', \
            'Другое']

        # Settings for 'a_dE_date' control element.
        self.addEventUi.a_dateEdit.setCalendarPopup(True)
        self.addEventUi.a_dateEdit.setDate(QDate(QDate.currentDate()))
        self.addEventUi.a_dateEdit.setMaximumDate(QDate(QDate.currentDate()))

        # Settings for 'a_cB_category' control element.
        self.addEventUi.a_comboBox.addItems(self.categs)

        # Connecting buttons to appropriate slots.
        self.addEventUi.a_btn_save.clicked.connect(self.add_event)
        self.addEventUi.a_btn_cancel.clicked.connect(self.addEventUi.close)
        self.addEventUi.a_btn_exit.clicked.connect(self.addEventUi.close)

    def add_event(self):
        # Get activities information entered by user. 
        event_title = self.addEventUi.a_lineEdit_name.text()
        event_category = self.addEventUi.a_comboBox.currentText()
        event_duration = self.addEventUi.a_lineEdit_time.text()
        event_date = datetime.now().strftime('%d/%m/%Y')   
        event_comment = self.addEventUi.a_te_comment.toPlainText()

        # Pushing obtained data to db
        self.timedb('database\\yurii_bel\\time_db.db').set_data(event_title, \
            event_category, event_duration, event_date, event_comment,\
                'Activity')  
        
        QtWidgets.QMessageBox.question(self,'Message', 
        "Активность успешно добавлена!", QtWidgets.QMessageBox.Ok)
        self.addEventUi.close()
        # self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = ActionsUI()
    sys.exit(app.exec())
    