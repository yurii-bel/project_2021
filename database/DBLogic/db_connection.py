from PyQt5 import uic
import psycopg2 as db
from psycopg2 import Error, connect
from uuid import uuid4
from peewee import *

database = 'deikj6tsb8tesq'
user = 'swvxsrergazlio'
password = 'd59791f7927ca5f5e8491bbbe93fbd93ea62e00a08821326f2aacc81c4307057'
host = 'ec2-54-216-185-51.eu-west-1.compute.amazonaws.com'


class UserConnection:
    def __init__(self):
        self.conn = db.connect(database=database, user=user,
                               password=password, host=host)
        self.cursor = self.conn.cursor()

        self.login_ui = uic.loadUi('design\\login_d.ui')

        # self.login_field_ui = self.lUi.login_lineedit_email.text()
        # self.password_field_ui = self.lUi.login_lineedit_password.text()

        self.user_login()
        # self.conn.close()

    def validation_check(self):
        pass

    def user_login(self, username):
        self.cursor.execute('SELECT COUNT(*) FROM "USER_NAME" WHERE \
            user_n_name = %s' % username)
        print(self.cursor.fetchall())

        # cursor.execute('SELECT USER_ID FROM "USER"')
        # results = cursor.fetchall()
        # print(results)


# class BaseModel(Model):
#     class Meta:
#         database = connection


# # Определяем модель исполнителя
# class User(BaseModel):
#     user_id = AutoField(column_name='user_id')
#     # name = TextField(column_name='Name', null=True)

#     class Meta:
#         table_name = 'User'


if __name__ == '__main__':
    uc = UserConnection()
    # dbl = User()
    # print(User.get(User.user_id == 1))
