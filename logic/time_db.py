import sys
sys.path.append(".")
import sqlite3

class TimeDb:
    def __init__(self):
        self.db = sqlite3.connect('database\\yurii_bel\\time_db.db')

        self.cursor = self.db.cursor()
    
    def set_data(self, *args, **kwargs):

        args_and_table = (args)  # arguments + table
        table_name = list(args_and_table).pop()  # table 
        args = list(args_and_table)[:-1]  # arguments - table
        prosseco = '?,'

        # pushing any number of arguments into db
        if len(args) == 1:
            prosseco = '?'
        elif len(args) == 2:
            prosseco += '?'
        elif len(args_and_table) >= 3:
            for i in range(len(args_and_table)-2):
                if i < len(args_and_table)-3:
                    prosseco += '?,'
                else:
                    prosseco += '?'

        self.cursor.execute(f'insert into {table_name} values({prosseco})', \
            args)
        self.db.commit()       


if __name__ == '__main__':
    time_db = TimeDb()
    time_db.set_data('dsa', 'q', '3', '4', '5', 'Activity')