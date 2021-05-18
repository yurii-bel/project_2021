import psycopg2


class DbLogic:

    def __init__(db_name, db_user, db_password, db_host, db_port):
        connection = None
        try:
            connection = psycorg2.connect(database = db_name,
            user = db_user,
            password = db_password,
            host = db_host,
            port = db_port)
            print('Successfull connection to database')
        except psycopg2.OperationalError as e:
            print(f'An error {e} occurred')

    def set_data():
        None

    def get_data():
        None

    def del_data():
        None

db_connect = DbLogic('Timesoft', 'postgres', '111', '127.0.0.1', '5432')