import re
import psycopg2 as db
from psycopg2 import Error
from uuid import uuid4
import psycopg2.extras


class DbLogic:

    database = 'dt1vdgsvah47r'
    user = 'ryxcgrjdgvrsxx'
    password = '2e4d8cbc5b0f94259507584c6868f20ae0d4da79fdc618f6c2602d18045b2b61'
    host = 'ec2-54-74-60-70.eu-west-1.compute.amazonaws.com'
# рабочий коннект

    def __init__(self):
        self.connection = db.connect(database=self.database,
                                     user=self.user,
                                     password=self.password,
                                     host=self.host)

        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        self.correct_login_info = False

    def set_data(self, table_name, column, *args):
        with self.connection:
            with self.cursor:
                table_name = table_name
                table_record = ', '.join(['%s']*len(args))
                insert_query = (f'(INSERT INTO "{table_name}" {column} VALUES {table_record})')
                self.cursor.execute(insert_query, args)

# наброски
    def get_data(self, table_name):
        with self.connection:
            with self.cursor:
                self.cursor.execute(f'(SELECT * FROM "{table_name}")')
                return self.cursor.fetchall()

    def get_data_selectively(self, table_name, column, condition):
        with self.connection:
            with self.cursor:
                self.cursor.execute(f'Select * FROM "{table_name}" WHERE {column} = %s;',(f'{condition}',))
                return self.cursor.fetchone()

    def del_data(self, table_name, condition):
        with self.connection:
            with self.cursor:
                self.cursor.execute(f'(DELETE FROM "{table_name}" WHERE {condition} ')


    # # timo364 get user id and add user info test methods.
    # def get_user_id(self, user):
    #     try:
    #         self.cursor.execute(
    #             'SELECT USER_N_ID FROM "USER_NAME"\
    #                 WHERE user_n_name = %(user)s', {'user': user})
    #         return self.cursor.fetchone()
    #     except (Exception, Error) as error:
    #         return f'{error}'
    #     finally:
    #         self.cursor.close()
    #         self.connection.close()

    # # TODO: Добавить проверки.
    # def register_user(self, user_n_name, user_p_email, user_p_password):
    #     try:
    #         user_n_id = str(uuid4())
    #         user_p_id = str(uuid4())
    #         self.connection.autocommit = True

    #         self.user_exists_bool, self.user_email_bool, self.user_empty_name_bool, \
    #             self.user_empty_email_bool, self.user_empty_password_bool = \
    #                 None, None, None, None, None

    #         self.user_exists_message, self.user_email_message, self.user_empty_name_message,\
    #             self.user_empty_email_message, self.user_empty_password_message = \
    #                 None, None, None, None, None

    #         self.cursor.execute(
    #             f'SELECT "USER_NAME".user_n_name = \'{user_n_name}\' FROM "USER_NAME"')
    #         # Сделано в Китае. Разработано в России.
    #         # Нужна проверка в основной.
    #         lst = str(self.cursor.fetchall())
    #         if 'True' in lst:
    #             self.user_exists_message = f'Данный пользователь уже зарегистрирован.'
    #             self.user_exists_bool = False
    #             return 

    #         # self.cursor.execute(
    #         #     f'SELECT "USER_PRIVATE".user_p_email = \'{user_p_email}\' FROM "USER_PRIVATE"')
    #         # # Сделано в Китае. Разработано в России.
    #         # # Нужна проверка в основной.
    #         # lst = str(self.cursor.fetchall())

    #         if 'True' in lst:
    #             self.user_email_message = f'Данный емейл уже зарегистрирован.'
    #             self.user_email_bool = False
    #             return

    #         if user_n_name == '':
    #             self.user_empty_name_message = f'Нельзя создать пустой логин пользователя.'
    #             self.user_empty_name_bool = False
    #             return

    #         if user_p_email == '':
    #             self.user_empty_email_message = f'Нельзя создать пустой емейл пользователя.'
    #             self.user_empty_email_bool = False
    #             return

    #         if user_p_password == '':
    #             self.user_empty_password_message = f'Нельзя создать пустой пароль пользователя.'
    #             self.user_empty_password_bool = False
    #             return
                

    #         self.cursor.execute('INSERT INTO "USER" (user_n_id, user_p_id)\
    #             VALUES (%s,%s) ON CONFLICT DO NOTHING', (user_n_id, user_p_id))

    #         self.cursor.execute('INSERT INTO "USER_NAME" (user_n_id, user_n_name)\
    #             VALUES (%s,%s) ON CONFLICT DO NOTHING', (user_n_id, user_n_name))

    #         self.cursor.execute('INSERT INTO "USER_PRIVATE" (user_p_id, user_p_email, user_p_password)\
    #             VALUES (%s,%s,%s) ON CONFLICT DO NOTHING', (user_p_id, user_p_email, user_p_password))



    #     except (Exception, Error) as error:
    #         return f'{error}'
    #     finally:
    #         self.cursor.close()
    #         self.connection.close()

    # def login_user(self, user_n_name, user_p_password):
    #     try:
    #         self.connection.autocommit = True

    #         self.current_user_id = None

    #         self.current_user_n_id = None
    #         self.current_user_n_name = None
    #         self.current_user_n_telegram = None

    #         self.current_user_p_id = None
    #         self.current_user_p_email = None
    #         self.current_user_p_password = None

    #         # working with USER_NAME table
    #         self.cursor.execute(
    #             f'SELECT user_n_id, user_n_name, user_n_telegram from "USER_NAME"')
    #         user_name_table_rows = self.cursor.fetchall()

    #         for row in user_name_table_rows:
    #             # print(f'\nuser_n_id: {row[0]} \nuser_n_name: {row[1]} \nuser_n_telegram: {row[2]}')
    #             if user_n_name == row[1]:
    #                 self.current_user_n_id = row[0]
    #                 self.current_user_n_name = row[1]
    #                 self.current_user_n_telegram = row[2]
    #                 break
    #             else:
    #                 pass

    #         # working with USER table
    #         self.cursor.execute(
    #             f'SELECT user_id, user_n_id, user_p_id from "USER"')
    #         user_table_rows = self.cursor.fetchall()

    #         for row in user_table_rows:
    #             if self.current_user_n_id == row[1]:
    #                 self.current_user_id = row[0]
    #                 self.current_user_p_id = row[2]
    #             else:
    #                 pass

    #         # working with USER_PRIVAT table
    #         self.cursor.execute(
    #             f'SELECT user_p_id, user_p_email, user_p_password from "USER_PRIVATE"')
    #         user_private_table_rows = self.cursor.fetchall()

    #         for row in user_private_table_rows:
    #             if user_p_password == row[2] and self.current_user_p_id == row[0]:
    #                 self.current_user_p_email = row[1]
    #                 self.current_user_p_password = row[2]
    #                 self.correct_login_info = True
    #                 break
    #             else:
    #                 self.correct_login_info = False

    #     except (Exception, Error) as error:
    #         return f'{error}'
    #     finally:
    #         self.cursor.close()
    #         self.connection.close()

    # def drop_user(self, user_n_name):
    #     try:
    #         self.connection.autocommit = True
    #         self.cursor.execute('DELETE FROM "USER_NAME" WHERE user_n_name = %(user)s',
    #                             {'user': user_n_name})

    #         self.connection.commit()

    #     except (Exception, Error) as error:
    #         return f'{error}'
    #     finally:
    #         self.cursor.close()
    #         self.connection.close()


if __name__ == '__main__':
    dbl = DbLogic()
    #print(dbl.get_data('ACTIVITY'))
    print(dbl.get_data_selectively('ACTIVITY','USER_ID', 4))
    # print(dbl.get_user_id('Sif'))
    # print(dbl.register_user('', 'wow@wow.ru', 'woooowowow'))
    # dbl.register_user('Leva9', 'leya9@ukr.net', 'qwerty9')
    # dbl.drop_user('Leva9')
    # print(dbl.login_user('John', 'ok john'))
