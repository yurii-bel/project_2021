import psycopg2 as db


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
db_conn = DbLogic()