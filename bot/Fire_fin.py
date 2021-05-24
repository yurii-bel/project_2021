tk = '1891194594:AAGDaHHTuZv5mDBIV8Q4Sjd7xU1RPPry0ns'
import psycopg2 as db
from telebot.types import User
import telebot

db_name='deikj6tsb8tesq'
db_pass='d59791f7927ca5f5e8491bbbe93fbd93ea62e00a08821326f2aacc81c4307057'
db_user='swvxsrergazlio'
db_host='ec2-54-216-185-51.eu-west-1.compute.amazonaws.com'

#подключение к бд на хироку
connection = db.connect(database=db_name, user=db_user, password=db_pass, host=db_host)

#подключение курсора для работы с бд
cur = connection.cursor()

#cur.execute('CREATE TABLE ACTIVITY(id SERIAL PRIMARY KEY, name VARCHAR);')
#cur.execute('INSERT INTO ACTIVITY (name) VALUES(%s)', ('eq',))
cur.execute('SELECT * FROM "USER";')

#вывод всех строк из таблицы
(cur.fetchall())

connection.commit()

cur.close()

connection.close()


bot = telebot.TeleBot(tk)



@bot.message_handler(commands=['start'])
def welcome_help(message):
    bot.send_message(message.chat.id, "Your'e started your bot")

#TODO:i need to fix 'connection'
#connection is lagged
@bot.message_handler(commands=['get_me'])
def get_message(message,connection):
    if message.chat.id == 'name':
        cursor = connection.cursor()
        cur.execute("SELECT * FROM USER_NAME  WHERE id = %s;",(2,))
        bot.send_message(message.chat.id, print(cur.fetchone().cursor))
        connection.commit()
        connection.close
    else:
        print('Please try again!')
    



if __name__ == '__main__':
    bot.infinity_polling(True)