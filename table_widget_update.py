from uuid import uuid4
from psycopg2 import Error
import psycopg2 as db
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys

import datetime


sys.path.append(".")

class TableWidget(QtWidgets.QTableWidget):

    database = 'dt1vdgsvah47r'
    user = 'ryxcgrjdgvrsxx'
    password = '2e4d8cbc5b0f94259507584c6868f20ae0d4da79fdc618f6c2602d18045b2b61'
    host = 'ec2-54-74-60-70.eu-west-1.compute.amazonaws.com'

    def __init__(self):
        self.connection = db.connect(database=self.database, user=self.user,\
            password=self.password, host=self.host)

        self.cursor = self.connection.cursor()

        self.tUi = uic.loadUi('design\\table.ui')  # Table ui.

        self.add_table_data()
        self.load_user_activities()
        self.load_table_data()

        # self.add_table_data2()
        # self.load_user_activities
        # self.load_table_data()


        self.tUi.show()

    def load_table_data(self):
        rows = self.table_rows_num

        self.tUi.tableW.setRowCount(rows)

        for i in range(rows):
            # setting all activities data.
            self.tUi.tableW.setItem(i, 0, 
            QtWidgets.QTableWidgetItem(self.activity_creation_date[i]))
            self.tUi.tableW.setItem(i, 1, 
            QtWidgets.QTableWidgetItem(self.activity_category[i]))
            self.tUi.tableW.setItem(i, 2, 
            QtWidgets.QTableWidgetItem(self.activity_name[i]))
            self.tUi.tableW.setItem(i, 3, 
            QtWidgets.QTableWidgetItem(self.activity_duration[i]))
            self.tUi.tableW.setItem(i, 4, 
            QtWidgets.QTableWidgetItem(self.activity_comment[i]))

        # Forbiding cell selection.
        self.tUi.tableW.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        # Resizing table columns to its contents.
        self.tUi.tableW.resizeColumnsToContents()

    def add_table_data(self):
        self.connection.autocommit = True
        cd = datetime.datetime.now().strftime("%m-%d-%Y")
        # print(cd)
        self.user_id = '12'
        self.actl_name = 'BUTTERFLY'
        self.act_time = 200
        self.act_date = cd
        self.cat_name = 'Спорт'
        self.act_comment = 'some shitt'

        self.cursor.execute('INSERT INTO "ACTIVITY_LIST" (user_id, actl_name, cat_name)\
                VALUES (%s,%s,%s) ON CONFLICT DO NOTHING',
                        (self.user_id, self.actl_name, self.cat_name))

        self.cursor.execute('INSERT INTO "ACTIVITY" (user_id, actl_name,\
            act_time, act_date, cat_name, act_comment)\
                VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING',
                        (self.user_id, self.actl_name, self.act_time, \
                            self.act_date, self.cat_name, self.act_comment))
        
    
    def add_table_data2(self):
        self.connection.autocommit = True
        cd = datetime.datetime.now().strftime("%m-%d-%Y")
        # print(cd)
        self.user_id = '12'
        self.actl_name = 'hmmmm updated'
        self.act_time = 200
        self.act_date = cd
        self.cat_name = 'Спорт'
        self.act_comment = 'some shitt'

        self.cursor.execute('INSERT INTO "ACTIVITY_LIST" (user_id, actl_name, cat_name)\
                VALUES (%s,%s,%s) ON CONFLICT DO NOTHING',
                        (self.user_id, self.actl_name, self.cat_name))

        self.cursor.execute('INSERT INTO "ACTIVITY" (user_id, actl_name,\
            act_time, act_date, cat_name, act_comment)\
                VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING',
                        (self.user_id, self.actl_name, self.act_time, \
                            self.act_date, self.cat_name, self.act_comment))
        
    



    def load_user_activities(self):
        # working with ACTIVITY table.
        self.activity_creation_date = []
        self.activity_category = []
        self.activity_name = []
        self.activity_duration = []
        self.activity_comment = []
        # The number of rows in current TableView widget.
        self.table_rows_num = 0

        self.connection.autocommit = True
        self.cursor.execute(
            f'SELECT act_id, user_id, actl_name, act_time, act_date, cat_name,\
                act_comment from "ACTIVITY" WHERE user_id = \'12\'')
        user_activities_table_rows = self.cursor.fetchall()
        # print(f':::: {user_activities_table_rows}')
        for row in user_activities_table_rows:
            if row[1] == 12:
                # print(f'row[1]: {row[1]} | self.current_user_id: {self.current_user_id:}')
                # print(f'act id: {row[0]}| id: {row[1]}| activity: {row[2]}' )
                self.activity_creation_date.append(str(row[4]))  # act_date
                self.activity_category.append(str(row[5]))  # cat_name
                self.activity_name.append(str(row[2]))  # actl_name
                self.activity_duration.append(str(row[3]))  # act_time
                self.activity_comment.append(str(row[6]))  # act_comment

        self.table_rows_num = len(self.activity_name)

    def reconnect_to_db(self):
        self.connection.close ()
        self.connection = db.connect(database=self.database, user=self.user,\
            password=self.password, host=self.host)

        self.cursor = self.connection.cursor()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = TableWidget()
    sys.exit(app.exec())