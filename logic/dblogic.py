import psycopg2 as db
from psycopg2 import Error
from uuid import uuid4
import psycopg2.extras


class DbLogic:

    database = 'dt1vdgsvah47r'
    user = 'ryxcgrjdgvrsxx'
    password = '2e4d8cbc5b0f94259507584c6868f20ae0d4da79fdc618f6c2602d18045b2b61'
    host = 'ec2-54-74-60-70.eu-west-1.compute.amazonaws.com'

    def __init__(self):
        self.connection = db.connect(database=self.database, user=self.user, \
        password=self.password, host=self.host)

        self.cursor = self.connection.cursor()
        self.cursor2 = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        self.correct_login_info = False
        self.user_input_check = None

    def register_user(self, user_n_name, user_p_email, user_p_password):
        try:
            user_n_id = str(uuid4())
            user_p_id = str(uuid4())
            self.connection.autocommit = True

            self.cursor.execute(
                f'SELECT "USER_NAME".user_n_name = \'{user_n_name}\' FROM "USER_NAME"')
            # Сделано в Китае. Разработано в России.
            lst = str(self.cursor.fetchall())
            if 'True' in lst:
                self.user_input_check = '1'
                return 
            elif 'True' in lst:
                self.user_input_check = '2'
                return
            elif user_n_name == '':
                self.user_input_check = '3'
                return
            elif user_p_email == '':
                self.user_input_check = '4'
                return
            elif user_p_password == '':
                self.user_input_check = '5'
                return
            elif len(user_p_password) <= 7:
                self.user_input_check = '6'
                return

            self.cursor.execute('INSERT INTO "USER" (user_n_id, user_p_id)\
                VALUES (%s,%s) ON CONFLICT DO NOTHING', (user_n_id, user_p_id))

            self.cursor.execute('INSERT INTO "USER_NAME" (user_n_id, user_n_name)\
                VALUES (%s,%s) ON CONFLICT DO NOTHING', (user_n_id, user_n_name))

            self.cursor.execute('INSERT INTO "USER_PRIVATE" (user_p_id, user_p_email, user_p_password)\
                VALUES (%s,%s,%s) ON CONFLICT DO NOTHING', (user_p_id, user_p_email, user_p_password))

        except Exception:
            pass

    def login_user(self, user_n_name, user_p_password):
        try:
            self.connection.autocommit = True

            self.current_user_id = None

            self.current_user_n_id = None
            self.current_user_n_name = None
            self.current_user_n_telegram = None

            self.current_user_p_id = None
            self.current_user_p_email = None
            self.current_user_p_password = None

            if user_n_name == '':
                self.user_input_check = '7'
                return
            elif user_p_password == '':
                self.user_input_check = '8'
                return

            # working with USER_NAME table
            self.cursor.execute(
                f'SELECT user_n_id, user_n_name, user_n_telegram from "USER_NAME"')
            user_name_table_rows = self.cursor.fetchall()

            for row in user_name_table_rows:
                if user_n_name == row[1]:
                    self.current_user_n_id = row[0]
                    self.current_user_n_name = row[1]
                    self.current_user_n_telegram = row[2]
                    break
                else:
                    pass

            # working with USER table
            self.cursor.execute(
                f'SELECT user_id, user_n_id, user_p_id from "USER"')
            user_table_rows = self.cursor.fetchall()

            for row in user_table_rows:
                if self.current_user_n_id == row[1]:
                    self.current_user_id = row[0]
                    self.current_user_p_id = row[2]
                else:
                    pass

            # working with USER_PRIVATE table
            self.cursor.execute(
                f'SELECT user_p_id, user_p_email, user_p_password from "USER_PRIVATE"')
            user_private_table_rows = self.cursor.fetchall()

            for row in user_private_table_rows:
                if user_p_password == row[2] and self.current_user_p_id == row[0]:
                    self.current_user_p_email = row[1]
                    self.current_user_p_password = row[2]
                    self.correct_login_info = True
                    break
                else:
                    self.correct_login_info = False

            if self.correct_login_info == True: 
                self.load_user_activities()   # loading activities from db

        except Exception:
            pass
    
    def load_user_activities(self):
        # working with ACTIVITY table.
        self.activity_creation_date = []
        self.activity_category = []
        self.activity_name = []
        self.activity_duration = []
        self.activity_comment = []
        self.table_rows_num = 0  # The number of rows in current TableView widget.

        try:
            self.connection.autocommit = True
            self.cursor.execute(
                f'SELECT act_id, user_id, actl_name, act_time, act_date, cat_name,\
                    act_comment from "ACTIVITY"')
            user_activities_table_rows = self.cursor.fetchall()
                
            for row in user_activities_table_rows:
                if row[1] == self.current_user_id:
                    # print(f'act id: {row[0]}| id: {row[1]}| activity: {row[2]}' )
                    self.activity_creation_date.append(str(row[4]))  # act_date
                    self.activity_category.append(str(row[5]))  # cat_name
                    self.activity_name.append(str(row[2]))  # actl_name
                    self.activity_duration.append(str(row[3]))  # act_time
                    self.activity_comment.append(str(row[6]))  # act_comment
            self.table_rows_num = len(self.activity_name)      
                    # print(f'{row[4]}')
            # print(f'\nDate: {self.activity_creation_date} \nCategory: \
            #     {self.activity_category} \nActivity: {self.activity_name} \
            #         \nDuration: {self.activity_duration} \nComment: {self.activity_comment}')
            

        except (Exception, Error) as error:
            return f'{error}'
        finally:
            self.cursor.close()
            self.connection.close()

    def drop_user(self, user_n_name):
        try:
            self.connection.autocommit = True
            
            user_id = self.get_user_n_id(user_n_name)

            self.cursor.execute(\
                'DELETE FROM "USER" WHERE user_n_id = %(userID)s',\
                                {'userID': user_id})
        except Exception:
            pass

    def get_user_n_id(self, user):
        try:
            self.cursor2.execute(
                'SELECT user_n_id FROM "USER_NAME"\
                    WHERE user_n_name = %(user)s', {'user': user})
            return str(self.cursor2.fetchone())[2:-2]
        except Exception:
            pass

    def get_user_id(self, user_n_id):
        try:
            self.cursor2.execute(\
                'SELECT user_id FROM "USER"\
                    WHERE user_n_id = %(user_n_id)s', {'user_n_id': user_n_id})
            return str(self.cursor2.fetchall())[2:-2]
        except Exception:
            pass

    def get_actl_id(self, user, actl_name, cat_name):
        self.connection.autocommit = True
        user_n_id = self.get_user_n_id(user)
        user_id = self.get_user_id(user_n_id)

        self.cursor2.execute(\
            f'SELECT actl_id FROM "ACTIVITY_LIST" WHERE\
                (user_id, actl_name, cat_name) = (\'{user_id}\', \'{actl_name}\', \'{cat_name}\')')
        for row in self.cursor2.fetchall():
            return row[0]

    def get_act_id(self, user, actl_name, act_time, act_date, cat_name, act_comment):
        self.connection.autocommit = True
        user_n_id = self.get_user_n_id(user)
        user_id = self.get_user_id(user_n_id)

        self.cursor2.execute(\
            f'SELECT act_id FROM "ACTIVITY" WHERE\
                (user_id, actl_name, act_time, act_date, cat_name, act_comment) =\
                    (\'{user_id}\', \'{actl_name}\', \'{act_time}\', \'{act_date}\',\
                        \'{cat_name}\', \'{act_comment}\')')
        for row in self.cursor2.fetchall():
            return row[0]

    def get_user_categories(self, user):
        try:
            self.connection.autocommit = True
            user_n_id = self.get_user_n_id(user)
            user_id = self.get_user_id(user_n_id)
            self.cursor2.execute(\
                'SELECT cat_name FROM "CATEGORY"\
                    WHERE user_id = %(userID)s', {'userID': user_id})
            categs = []
            for row in self.cursor2.fetchall():
                categs += row
            return categs
        except Exception:
            pass

    def copy_user(self, table_name, column):
        try:
            with self.connection:
                with self.cursor:
                    self.cursor.execute(f'SELECT * FROM "{table_name}"\
                        WHERE USER_ID = \'{column}\'')
                    return self.cursor.fetchall()
        except (Exception, Error) as error:
            return f'{error}'

    def add_event(self, user, actl_name, act_time, act_date, cat_name,\
        act_comment):

        self.connection.autocommit = True
        user_n_id = self.get_user_n_id(user)
        user_id = self.get_user_id(user_n_id)

        self.cursor2.execute(\
            f'SELECT cat_name FROM "CATEGORY" WHERE user_id = \'{user_id}\'')
        user_categories = self.cursor2.fetchall()
        for row in user_categories:
            if cat_name == row[0]:
                break
        else:
            self.cursor2.execute(\
                f'INSERT INTO "CATEGORY" (user_id, cat_name) VALUES (%s,%s)',\
                    (user_id, cat_name))

        self.cursor2.execute(\
            f'INSERT INTO "ACTIVITY_LIST" (user_id, actl_name, cat_name)\
                VALUES (%s,%s,%s)', (user_id, actl_name, cat_name))

        self.cursor2.execute('INSERT INTO "ACTIVITY" (user_id, actl_name,\
                    act_time, act_date, cat_name, act_comment)\
                        VALUES (%s,%s,%s,%s,%s,%s)',\
                    (user_id, actl_name, act_time, act_date, cat_name, act_comment))

    def edit_event(self, user, actl_name, act_time, act_date, cat_name,\
        act_comment, act_id, actl_id):

        self.connection.autocommit = True
        user_n_id = self.get_user_n_id(user)
        user_id = self.get_user_id(user_n_id)

        self.cursor2.execute(\
            f'SELECT cat_name FROM "CATEGORY" WHERE user_id = \'{user_id}\'')
        user_categories = self.cursor2.fetchall()
        for row in user_categories:
            if cat_name == row[0]:
                break
        else:
            self.cursor2.execute(\
                f'INSERT INTO "CATEGORY" (user_id, cat_name) VALUES (%s,%s)',\
                    (user_id, cat_name))

        self.cursor2.execute(\
            f'UPDATE "ACTIVITY_LIST" SET (actl_name, cat_name) = (\'{actl_name}\',\
                \'{cat_name}\') WHERE actl_id = \'{actl_id}\'')
        
        self.cursor2.execute(\
            f'UPDATE "ACTIVITY" SET (actl_name, act_time, act_date, cat_name, \
                act_comment) = (\'{actl_name}\', \'{act_time}\', \'{act_date}\',\
                    \'{cat_name}\', \'{act_comment}\') WHERE act_id = \'{act_id}\'')

    def drop_event(self, user, actl_name):
        try:
            self.connection.autocommit = True
            user_n_id = self.get_user_n_id(user)
            user_id = self.get_user_id(user_n_id)

            self.cursor2.execute(\
                f'DELETE FROM "ACTIVITY"\
                    WHERE user_id = \'{user_id}\' and actl_name = \'{actl_name}\'')

            self.cursor2.execute(\
                f'DELETE FROM "ACTIVITY_LIST"\
                    WHERE user_id = \'{user_id}\' and actl_name = \'{actl_name}\'')
        except Exception:
            pass

    def drop_category(self, user, cat_name):
        try:
            self.connection.autocommit = True
            user_n_id = self.get_user_n_id(user)
            user_id = self.get_user_id(user_n_id)

            self.cursor2.execute(\
                f'DELETE FROM "CATEGORY"\
                    WHERE user_id = \'{user_id}\' and cat_name = \'{cat_name}\'')
        except Exception:
            pass

if __name__ == '__main__':
    dbl = DbLogic()
    # print(dbl.get_user_n_id('Тимофей'))
    # print(dbl.register_user('', 'wow@wow.ru', 'woooowowow'))
    # dbl.register_user('Leva9', 'leya9@ukr.net', 'qwerty91')
    # dbl.drop_user('Leva9')
    # print(dbl.login_user('John', 'ok john'))
    # print(dbl.get_user_categories('Timofey'))
    # print(dbl.copy_user('CATEGORY', '2'))
    # dbl.add_event('Timofey', 'Прогулка', '60', '2021-03-31', 'Отдых', 'Вражений')
    # dbl.drop_event('Timofey', 'Катание на лыжах')
    # dbl.drop_category('Timofey', 'Спорт')
    # print(dbl.get_user_categories('Sif'))
    # print(dbl.copy_user('CATEGORY', '2'))
    # print(dbl.get_actl_id('Timofey', 'Бег', 'Спорт'))
    # print(dbl.get_act_id('Timofey', 'Бег', '60', '2021-05-26', 'Спорт', 'Набегался!'))
