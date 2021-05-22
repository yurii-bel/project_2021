import psycopg2 as db

db_name = 'deikj6tsb8tesq'
db_pass = 'd59791f7927ca5f5e8491bbbe93fbd93ea62e00a08821326f2aacc81c4307057'
db_user = 'swvxsrergazlio'
db_host = 'ec2-54-216-185-51.eu-west-1.compute.amazonaws.com'

# подключение к бд на хироку
connection = db.connect(database=db_name, user=db_user,
                        password=db_pass, host=db_host)

# подключение курсора для работы с бд
cur = connection.cursor()

#cur.execute('CREATE TABLE ACTIVITY(id SERIAL PRIMARY KEY, name VARCHAR);')
#cur.execute('INSERT INTO ACTIVITY (name) VALUES(%s)', ('eq',))
cur.execute('SELECT * FROM "USER";')

# вывод всех строк из таблицы
print(cur.fetchall())

connection.commit()

cur.close()

connection.close()
