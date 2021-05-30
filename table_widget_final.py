from PyQt5 import QtSql
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QCheckBox, QComboBox, QHBoxLayout, QInputDialog, QMessageBox, QPushButton, QTableView, QVBoxLayout, QWidget
from uuid import uuid4
from psycopg2 import Error
import psycopg2 as db
# from PyQt5 import QtCore, QtGui, QtWidgets, uic, QtQsl

import datetime

import sys

class TableWidget(QWidget):

    database = 'dt1vdgsvah47r'
    user = 'ryxcgrjdgvrsxx'
    password = '2e4d8cbc5b0f94259507584c6868f20ae0d4da79fdc618f6c2602d18045b2b61'
    host = 'ec2-54-74-60-70.eu-west-1.compute.amazonaws.com'

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # # db connection
        # self.connection = db.connect(database=self.database, user=self.user,\
        #     password=self.password, host=self.host)
        # self.cursor = self.connection.cursor()

        self.qsqldb = QSqlDatabase().addDatabase('QPSQL')
        

        self.qsqldb.setHostName(self.host);
        self.qsqldb.setDatabaseName(self.database);
        self.qsqldb.setPassword(self.password);
        self.qsqldb.setUserName(self.user);
        self.qsqldb.open()

        self.model = QSqlTableModel(self, self.qsqldb)
        self.model.setTable("names")
        self.model.setHeaderData(0, Qt.Horizontal, "Дата")
        self.model.setHeaderData(1, Qt.Horizontal, "Категория")
        self.model.setHeaderData(2, Qt.Horizontal, "Активность")
        self.model.setHeaderData(3, Qt.Horizontal, "Продолжительность")
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.select()

        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.view.setSelectionBehavior(QAbstractItemView.SelectRows)
        #self.view.setColumnHidden(0, True)
        self.view.resizeColumnsToContents()
        self.view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.view.horizontalHeader().setStretchLastSection(True)

        addButton = QPushButton("Add")
        editButton = QPushButton("Edit")
        deleteButton = QPushButton("Delete")
        exitButton = QPushButton("Exit")

        hbox = QHBoxLayout()
        hbox.addWidget(addButton)
        hbox.addWidget(editButton)
        hbox.addWidget(deleteButton)
        hbox.addStretch()
        hbox.addWidget(exitButton)

        vbox = QVBoxLayout()
        vbox.addWidget(self.view)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        addButton.clicked.connect(self.addRecord)
        #editButton.clicked.connect(self.editRecord) # omitted for simplicity
        deleteButton.clicked.connect(self.deleteRecord) # omitted for simplicity
        # self.checkbox.clicked.connect(self.checkBoxCloseDatabase)
        exitButton.clicked.connect(self.close)

    # def 

    def addRecord(self):
        # self.
        # self.connection.autocommit = True
        cd = datetime.datetime.now().strftime("%m-%d-%Y")
        # print(cd)
        self.user_id = '12'
        self.actl_name = 'BUTTERFLY'
        self.act_time = 200
        self.act_date = cd
        self.cat_name = 'Спорт'
        self.act_comment = 'some shitt'

        row = self.model.rowCount()
        self.model.insertRow(row)
        self.model.setData(self.model.index(row, 1), self.act_date)
        self.model.setData(self.model.index(row, 2), self.actl_name)
        self.model.setData(self.model.index(row, 3), self.cat_name)
        self.model.setData(self.model.index(row, 4), self.act_time)

        if self.model.submitAll():
            self.connection.commit()
            self.view.setCurrentIndex(self.model.index(row, 1))
            self.view.setCurrentIndex(self.model.index(row, 2))
            self.view.setCurrentIndex(self.model.index(row, 3))
            self.view.setCurrentIndex(self.model.index(row, 4))
        else:
            self.model.revertAll()
            self.connection.rollback()
            QMessageBox.warning(self, "Error", "Database not available. Please, try again later.")




        # query.prepare('INSERT INTO "ACTIVITY_LIST" (user_id, actl_name, cat_name)\
        #         VALUES (%s,%s,%s) ON CONFLICT DO NOTHING',
        #                 (self.user_id, self.actl_name, self.cat_name))
        # query.bindValue("user_id", self.user_id)
        # query.bindValue("actl_name", self.actl_name)
        # query.bindValue("cat_name", self.cat_name)


        # query.prepare('INSERT INTO "ACTIVITY" (user_id, actl_name,\
        #     act_time, act_date, cat_name, act_comment)\
        #         VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING',
        #                 (self.user_id, self.actl_name, self.act_time, \
        #                     self.act_date, self.cat_name, self.act_comment))


        # if query.exec_():
        #     self.model.select()
        # else:
        #     pass

    def closeDatabase():
        db.close()

    def deleteRecord(self):
        query = QSqlQuery(self.qsqldb)
        query.exec_('SELECT actl_name, cat_name FROM "ACTIVITY" WHERE user_id = \'12\'')
        index = query.record().indexOf('actl_name')
        rows = []
        while query.next():
            rows.append(query.value(index))
        print(rows)

        query.exec_('SELECT user_n_name FROM "USER_NAME" WHERE user_n_id\
             = \'a335e09a-1dc0-4187-9ad5-9fc92f0f7bfa\'')
        index = query.record().indexOf('user_n_name')
        rows.clear()
        while query.next():
            rows.append(query.value(index))
        print(rows)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TableWidget()
    window.resize(800, 500)
    window.show()
    sys.exit(app.exec())
    # app.exec_()