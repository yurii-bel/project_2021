import psycopg2 as db
from psycopg2 import Error
from uuid import uuid4


class DbLogic:

    database = 'deikj6tsb8tesq'
    user = 'swvxsrergazlio'
    password = 'd59791f7927ca5f5e8491bbbe93fbd93ea62e00a08821326f2aacc81c4307057'
    host = 'ec2-54-216-185-51.eu-west-1.compute.amazonaws.com'
#рабочий коннект
    def __init__(self):
        self.connection = db.connect(database = self.database,
                                            user = self.user,
                                            password = self.password,
                                            host = self.host)

        self.cursor = self.connection.cursor()

#Не трогать, не работает пока что
    # def set_data(self, table_name, stolbec, *args):
    #     table_name = table_name
    #     table_record = ', '.join(['%s']*len(args))
    #     insert_query = (f'(INSERT INTO "{table_name}" {stolbec} VALUES {table_record})')
    #     self.connection.autocommit = True
    #     cursor = self.connection.cursor()
    #     cursor.execute(insert_query, args)

#наброски
    def get_data(self, table_name):
        self.cursor.execute(f'(SELECT * FROM "{table_name}")')
        return self.cursor.fetchall()

    def del_data(self, table_name, condition):
        self.cursor.execute(f'(DELETE FROM "{table_name}" WHERE {condition} ')
        return self.cursor.fetchall()

    def __stop__(self):
        self.connection.close()

    # timo364 get user id and add user info test methods.
    def get_user_id(self, user):
        try:
            self.cursor.execute(\
                'SELECT USER_N_ID FROM "USER_NAME"\
                    WHERE user_n_name = %(user)s', {'user':user})
            return self.cursor.fetchone()
        except (Exception, Error) as error:
            return f'{error}'
        finally:
            self.cursor.close()
            self.connection.close()

    #TODO: Добавить проверки.
    def register_user(self, user_n_name, user_p_email, user_p_password):
        try:
            user_n_id = str(uuid4())
            user_p_id = str(uuid4())
            self.connection.autocommit = True

            self.cursor.execute(\
                f'SELECT "USER_NAME".user_n_name = \'{user_n_name}\' FROM "USER_NAME"')
            # Сделано в Китае. Разработано в России.
            # Нужна проверка в основной.
            lst = str(self.cursor.fetchall())
            if 'True' in lst:
                return f'Данный пользователь уже зареган.'

            self.cursor.execute(\
                f'SELECT "USER_PRIVAT".user_p_email = \'{user_p_email}\' FROM "USER_PRIVAT"')
            # Сделано в Китае. Разработано в России.
            # Нужна проверка в основной.
            lst = str(self.cursor.fetchall())
            if user_n_name == '':
                return f'Нельзя создать пустого пользователя.'
            if 'True' in lst:
                return f'Данное мыло уже зарегано.'

            self.cursor.execute('INSERT INTO "USER" (user_n_id, user_p_id)\
             VALUES (%s,%s) ON CONFLICT DO NOTHING', (user_n_id, user_p_id))

            self.cursor.execute('INSERT INTO "USER_NAME" (user_n_id, user_n_name)\
                VALUES (%s,%s) ON CONFLICT DO NOTHING', (user_n_id, user_n_name))
                
            self.cursor.execute('INSERT INTO "USER_PRIVAT" (user_p_id, user_p_email, user_p_password)\
                VALUES (%s,%s,%s) ON CONFLICT DO NOTHING', (user_p_id, user_p_email, user_p_password))
            
        except (Exception, Error) as error:
            return f'{error}'
        finally:
            self.cursor.close()
            self.connection.close()

    def login_user(self, user_n_name, user_p_password):
        try:
            self.connection.autocommit = True

            self.cursor.execute(\
                f'SELECT "USER_NAME".user_n_name = \'{user_n_name}\' FROM "USER_NAME"')
            # Сделано в Китае. Разработано в России.
            lst = str(self.cursor.fetchall())
            if not 'True' in lst:
                return f'Данный пользователь не найден. Зарегестрируйтесь.'

            self.cursor.execute(\
                f'SELECT user_n_name, user_p_password FROM "USER_NAME", "USER_PRIVAT"\
                    WHERE user_n_name = \'{user_n_name}\'\
                        and user_p_password = \'{user_p_password}\'')

            lst = self.cursor.fetchall()
            if lst == []:
                return f'Неверный пароль.'
            else:
                return lst
        except (Exception, Error) as error:
            return f'{error}'
        finally:
            self.cursor.close()
            self.connection.close()

    def drop_user(self, user_n_name):
        try:
            self.connection.autocommit = True
            self.cursor.execute('DELETE FROM "USER_NAME" WHERE user_n_name = %(user)s',\
                {'user':user_n_name})
            
            self.connection.commit()
        except (Exception, Error) as error:
            return f'{error}'
        finally:
            self.cursor.close()
            self.connection.close()
        

if __name__ == '__main__':
    dbl = DbLogic()
    # print(dbl.get_user_id('Sif'))
    # print(dbl.register_user('', 'wow@wow.ru', 'woooowowow'))
    # dbl.register_user('Leva9', 'leya9@ukr.net', 'qwerty9')
    # dbl.drop_user('Leva9')
    print(dbl.login_user('John', 'ok john'))
