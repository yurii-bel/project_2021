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

        self.user_exists_bool, self.user_email_bool, self.user_empty_name_bool,\
            self.user_empty_email_bool, self.user_empty_password_bool,\
                self.user_incorrect_password_bool =\
                    None, None, None, None, None, None

        self.user_exists_message, self.user_email_message,\
            self.user_empty_name_message, self.user_empty_email_message,\
                self.user_empty_password_message,\
                    self.user_incorrect_password_message =\
                        None, None, None, None, None, None


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
                self.user_exists_message = f'Данный пользователь уже зарегистрирован.'
                self.user_exists_bool = False
                return 
            elif 'True' in lst:
                self.user_email_message = f'Данный емейл уже зарегистрирован.'
                self.user_email_bool = False
                return
            elif user_n_name == '':
                self.user_empty_name_message = f'Нельзя создать пустой логин пользователя.'
                self.user_empty_name_bool = False
                return
            elif user_p_email == '':
                self.user_empty_email_message = f'Нельзя создать пустой емейл пользователя.'
                self.user_empty_email_bool = False
                return
            elif user_p_password == '':
                self.user_empty_password_message = f'Нельзя создать пустой пароль пользователя.'
                self.user_empty_password_bool = False
                return
            elif len(user_p_password) <= 7:
                self.user_incorrect_password_message =\
                    f'Длина пароля должна быть не менее 8 символов.'
                self.user_incorrect_password_bool = False
                return


            self.cursor.execute('INSERT INTO "USER" (user_n_id, user_p_id)\
                VALUES (%s,%s) ON CONFLICT DO NOTHING', (user_n_id, user_p_id))

            self.cursor.execute('INSERT INTO "USER_NAME" (user_n_id, user_n_name)\
                VALUES (%s,%s) ON CONFLICT DO NOTHING', (user_n_id, user_n_name))

            self.cursor.execute('INSERT INTO "USER_PRIVATE" (user_p_id, user_p_email, user_p_password)\
                VALUES (%s,%s,%s) ON CONFLICT DO NOTHING', (user_p_id, user_p_email, user_p_password))

        except (Exception, Error) as error:
            return f'{error}'
        finally:
            self.cursor.close()
            self.connection.close()

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
                self.user_empty_name_message =\
                    f'Строка логина пуста. Пожалуйста, введите Ваш логин.'
                self.user_empty_name_bool = False
                return
            elif user_p_password == '':
                self.user_empty_password_message =\
                    f'Строка с паролем пуста. Пожалуйста, введите Ваш пароль.'
                self.user_empty_password_bool = False
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

        except (Exception, Error) as error:
            return f'{error}'
        finally:
            self.cursor.close()
            self.connection.close()

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

            self.connection.commit()

        except (Exception, Error) as error:
            return f'{error}'
        finally:
            self.cursor.close()
            self.connection.close()

    def get_user_n_id(self, user):
        try:
            self.cursor.execute(
                'SELECT user_n_id FROM "USER_NAME"\
                    WHERE user_n_name = %(user)s', {'user': user})
            return str(self.cursor.fetchone())[2:-3]
        except (Exception, Error) as error:
            return f'{error}'

    def get_user_id(self, user_n_id):
        self.cursor.execute(\
            'SELECT user_id FROM "USER"\
                WHERE user_n_id = %(user_n_id)s', {'user_n_id': user_n_id})
        return str(self.cursor.fetchall())[2:-3]
        # except (Exception, Error) as error:
        #     return f'{error}'

    def get_user_categories(self, user):
        try:
            user_n_id = self.get_user_n_id(user)
            user_id = self.get_user_id(user_n_id)
            self.cursor.execute(\
                'SELECT cat_name FROM "CATEGORY"\
                    WHERE user_id = %(userID)s', {'userID': user_id})
            return str(self.cursor.fetchall())
        except (Exception, Error) as error:
            return f'{error}'
        finally:
            self.cursor.close()
            self.connection.close()

    def copy_user(self, table_name, column):
        # try:
        with self.connection:
            with self.cursor:
                self.cursor.execute(f'SELECT * FROM "{table_name}"\
                    WHERE USER_ID = \'{column}\'')
                return self.cursor.fetchall()
    # except (Exception, Error) as error:
        #     return f'{error}'
        # finally:
        #     self.cursor.close()
        #     self.connection.close()


if __name__ == '__main__':
    dbl = DbLogic()
    # print(dbl.get_user_n_id('Тимофей'))
    # print(dbl.register_user('', 'wow@wow.ru', 'woooowowow'))
    # dbl.register_user('Leva9', 'leya9@ukr.net', 'qwerty91')
    # dbl.drop_user('Leva9')
    # print(dbl.login_user('John', 'ok john'))
    # print(dbl.get_user_categories('Sif'))
    # print(dbl.copy_user('CATEGORY', '2'))
