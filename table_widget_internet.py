import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QCheckBox, QComboBox, QHBoxLayout, QInputDialog, QMessageBox, QPushButton, QTableView, QVBoxLayout, QWidget

class Window(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.model = QSqlTableModel(self)
        self.model.setTable("names")
        self.model.setHeaderData(0, Qt.Horizontal, "Id")
        self.model.setHeaderData(1, Qt.Horizontal, "Name")
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
        self.combo = QComboBox()
        self.combo.addItem("1) 1.Database, 2.Model (select)")
        self.combo.addItem("2) 1.Model, 2.Database")
        self.combo.addItem("3) 1.Database, 2.Model (insert)")
        self.combo.setCurrentIndex (0)
        self.checkbox = QCheckBox("Database Closed")

        hbox = QHBoxLayout()
        hbox.addWidget(addButton)
        hbox.addWidget(editButton)
        hbox.addWidget(deleteButton)
        hbox.addWidget(self.combo)
        hbox.addWidget(self.checkbox)
        hbox.addStretch()
        hbox.addWidget(exitButton)

        vbox = QVBoxLayout()
        vbox.addWidget(self.view)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        addButton.clicked.connect(self.addRecord)
        #editButton.clicked.connect(self.editRecord) # omitted for simplicity
        #deleteButton.clicked.connect(self.deleteRecord) # omitted for simplicity
        self.checkbox.clicked.connect(self.checkBoxCloseDatabase)
        exitButton.clicked.connect(self.close)

    def checkBoxCloseDatabase(self):
        if self.checkbox.isChecked():
            closeDatabase()
        else:
            pass
            #db.open() # it doesn't work

    def addRecord(self):
        # just QInputDialog for simplicity
        value, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter the name:')
        if not ok:
            return

        # Now, what is the best way to insert the record?

        if self.combo.currentIndex() == 0:
            # 1st approach, first in database, then model.select()
            # it seems like the most natural way to me
            query = QSqlQuery()
            query.prepare("INSERT INTO names (name) VALUES(:name)")
            query.bindValue( ":name", value )
            if query.exec_():
                self.model.select() # now we know the record is inserted to db
                # the problem with this approach is that select() can be slow
                # somehow position the view to newly added record?!
            else:
                pass
                # message to user
                # if the record can't be inserted to database,
                # there's no way I will show that record in view
        elif self.combo.currentIndex() == 1:
            # 2nd approach, first in view (model cache), then in database
            QSqlDatabase.database().transaction()
            row = self.model.rowCount()
            self.model.insertRow(row)
            self.model.setData(self.model.index(row, 1), value)
            #self.model.submit()
            if self.model.submitAll():
                QSqlDatabase.database().commit()
                self.view.setCurrentIndex(self.model.index(row, 1))
            else:
                self.model.revertAll()
                QSqlDatabase.database().rollback()
                QMessageBox.warning(self, "Error", "Database not available. Please, try again later.")

        else:
            # 3rd approach, first in database, then model.insertRow()
            # it is not a complete solution and is not so practical
            query = QSqlQuery()
            query.prepare("INSERT INTO names (name) VALUES(:name)")
            query.bindValue( ":name", value )
            if query.exec_():
                #id = ... # somehow find id from the newly added record in db
                row = self.model.rowCount()
                self.model.insertRow(row)
                #self.model.setData(self.model.index(row, 0), id) # we don't know it
                self.model.setData(self.model.index(row, 1), value)
                # not a complete solution
            else:
                pass
                # do nothing, because model isn't changed
                # message to user

def closeDatabase():
    db.close()

def createFakeData():
    query = QSqlQuery()
    query.exec_("DROP TABLE names")
    query.exec_("CREATE TABLE names(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, name TEXT)")
    query.exec_("INSERT INTO names VALUES(1, 'George')")
    query.exec_("INSERT INTO names VALUES(2, 'Rita')")
    query.exec_("INSERT INTO names VALUES(3, 'Jane')")
    query.exec_("INSERT INTO names VALUES(4, 'Steve')")
    query.exec_("INSERT INTO names VALUES(5, 'Maria')")
    query.exec_("INSERT INTO names VALUES(6, 'Bill')")
    #import random
    #for i in range(1000):
    #    name = chr(random.randint(65, 90))
    #    for j in range(random.randrange(3, 10)):
    #        name += chr(random.randint(97, 122))
    #
    #    query.prepare("INSERT INTO names (name) VALUES(:name)")
    #    query.bindValue( ":name", name )
    #    query.exec_()

app = QApplication(sys.argv)
db = QSqlDatabase.addDatabase("QSQLITE")
#db.setDatabaseName("test.db")
db.setDatabaseName(":memory:")
#openDatabase()
db.open()
createFakeData()
window = Window()
window.resize(800, 500)
window.show()
app.exec_()