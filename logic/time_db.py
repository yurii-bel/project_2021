import sys
sys.path.append(".")
import sqlite3

class TimeDb:
    def __init__(self):
        self.db = sqlite3.connect('database\\yurii_bel\\time_db.db')

        self.cursor = self.db.cursor()
    
    def set_user_data(self, *args, **kwargs):

        args_and_table = (args)  # arguments + table
        table_name = list(args_and_table)[-1]  # table 
        args = list(args_and_table).pop()  # aeguments - table
        prosseco = '?,'

        # pushing any number of arguments into db
        for i in range(len(args_and_table)-2):
            if i < len(args_and_table)-3:
                prosseco += '?,'
            else:
                prosseco += '?'
        
        print(type(args_and_table))
        self.cursor.execute(f'insert into {table_name} values({prosseco})', \
            args)
        self.db.commit()       

    



if __name__ == '__main__':
    time_db = TimeDb()
    time_db.set_user_data('dsa', 'em@gmail.com', '123', '32jd2dj', 'User')