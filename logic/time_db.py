import sys
sys.path.append(".")
import sqlite3

class TimeDb:
    def __init__(self, db):
        self.db = sqlite3.connect(f'{db}')
        self.cursor = self.db.cursor()
    
    def set_data(self, *args):
        args_and_table = (args)  # arguments + table
        table_name = list(args_and_table).pop()  # table 
        args = list(args_and_table)[:-1]  # arguments - table
        symbol = '?,'

        # pushing any number of arguments into db
        if len(args) == 1:
            symbol = '?'
        elif len(args) == 2:
            symbol += '?'
        elif len(args_and_table) >= 3:
            for i in range(len(args_and_table)-2):
                if i < len(args_and_table)-3:
                    symbol += '?,'
                else:
                    symbol += '?'

        self.cursor.execute(f'insert into {table_name} values({symbol})', \
            args)
        self.db.commit()       

    def get_data(self, *args):
        args_and_table = (args)  # arguments + table
        table_name = list(args_and_table).pop()  # table 
        args = list(args_and_table)[:-1]  # arguments - table

        sql = f'SELECT {str(args)[2:-2]} FROM {table_name}'
        self.cursor.execute(sql)
        full_data = self.cursor.fetchall()
        return str(full_data)[3:-4]

    # def get_data_where_user(self, *args):
    #     args_and_table = (args)  # arguments + table.
    #     table_name = list(args_and_table).pop()  # table.
    #     args_ = str(list(args_and_table)[0:-1])  # arguments - table and user id.
    #     user_id = str(list(args_and_table)[0]) # user id.
   
    #     sql = f'SELECT {str(args)[2:-2]} FROM {table_name} WHERE user_id = {user_id}'
    #     print(args_and_table)
    #     print(table_name)
    #     print(args_)
    #     print(user_id)
    #     # self.cursor.execute(sql)
    #     # full_data = self.cursor.fetchall()
    #     # return str(full_data)[3:-4]

    def del_data(self, *args):
        args_and_table = (args)  # arguments + table
        table_name = list(args_and_table).pop()  # table 
        args = list(args_and_table)[:-1]  # arguments - table
        args_first = args[0]
        args_second = args[1]

        sql = f'DELETE FROM {table_name} WHERE {args_first} = "{args_second}"'
        self.cursor.execute(sql)
        self.db.commit()

    def custom_sql(self, sql=str):
        sql_ = sql
        self.cursor.execute(sql_)
        self.db.commit()


if __name__ == '__main__':
    time_db = TimeDb('database\\yurii_bel\\time_db.db')
     # time_db.set_data('John', 'john@gmail.com', '123', 'telegramm', 'User')
     # time_db.get_data('user_email', 'User')
     # time_db.del_data('user_name', 'John', 'User')
    time_db.get_data_where_user('43', 'user_id', 'Activity')