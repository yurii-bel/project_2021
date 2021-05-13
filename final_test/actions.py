import sys
from design.new_editUI import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableView
from PyQt5 import QtSql
from PyQt5 import QtCore
from datetime import datetime



class form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.now = datetime.now()
        self.current_date = self.now.strftime("%d/%m/%Y %H:%M:")

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('fieldlist.db')
        self.model = QtSql.QSqlTableModel()
        self.model.setTable('field')
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()
        self.model.setHeaderData(0, QtCore.Qt.Horizontal,"id")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal,"Название события")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal,"Категория")
        self.model.setHeaderData(3, QtCore.Qt.Horizontal,"Потрачено времени")
        self.model.setHeaderData(4, QtCore.Qt.Horizontal,"Дата создания")
        self.ui.tableWidget.setModel(self.model)
        self.ui.button_add.clicked.connect(self.addToDb)
        
        self.ui.button_refresh.clicked.connect(self.updaterow)
        self.ui.button_delete.clicked.connect(self.delrow)
        self.i = self.model.rowCount()
        self.ui.lcdNumber.display(self.i)
        print(self.ui.tableWidget.currentIndex().row())
        self.show()

    def addToDb(self):
        print(self.i)
        self.model.insertRows(self.i,1)
        self.model.setData(self.model.index(self.i,1), 
        self.ui.lineEdit_action_name.text())  # add text to db from action_name
        self.model.setData(self.model.index(self.i,2),
        self.ui.comboBox.currentText())  # str? # add text to db from comboBox
        self.model.setData(self.model.index(self.i,3),
        self.ui.lineEdit_spend_time())  # add text to db from spend_time
        self.model.setData(self.model.index(self.i,4), 
        self.current_date)  # add text of today's date to db 
        self.model.submitAll()
        self.i += 1
        self.ui.lcdNumber.display(self.i)

    def delrow(self):
        if self.ui.tableWidget.currentIndex().row() > -1:
            self.model.removeRow(self.ui.tableWidget.currentIndex().row())
            self.i -= 1
            self.model.select()
            self.ui.lcdNumber.display(self.i)
        else:
            QMessageBox.question(self,'Message', 
            "Пожалуйста, выберите строку для удаления", QMessageBox.Ok)
            self.show()

    def updaterow(self):
        if self.ui.tableWidget.currentIndex().row() > -1:
            record = self.model.record(self.ui.tableWidget.currentIndex().row())
            record.setValue("Название события",self.ui.lineEdit_action_name)
            record.setValue("Категория",self.ui.comboBox.currentText())
            record.setValue("Потрачено времени", self.ui.lineEdit_spend_time)
            record.setValue("Дата создания", self.current_date)
            self.model.setRecord(self.ui.tableWidget.currentIndex().row(), record)
        else:
            QMessageBox.question(self,'Message', 
            "Пожалуйста, выберите строку для обновления", QMessageBox.Ok)
            self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frm = form()
    sys.exit(app.exec_())
