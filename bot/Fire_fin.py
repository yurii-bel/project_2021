import telebot
from telebot.types import User
import psycopg2 as db
tk = '1891194594:AAGDaHHTuZv5mDBIV8Q4Sjd7xU1RPPry0ns'

database = 'dt1vdgsvah47r'
user = 'ryxcgrjdgvrsxx'
password = '2e4d8cbc5b0f94259507584c6868f20ae0d4da79fdc618f6c2602d18045b2b61'
host = 'ec2-54-74-60-70.eu-west-1.compute.amazonaws.com'

# подключение к бд на хироку
connection = db.connect(database=db_name, user=db_user,
                        password=db_pass, host=db_host)

# подключение курсора для работы с бд
cur = connection.cursor()

#cur.execute('CREATE TABLE ACTIVITY(id SERIAL PRIMARY KEY, name VARCHAR);')
#cur.execute('INSERT INTO ACTIVITY (name) VALUES(%s)', ('eq',))
cur.execute('SELECT * FROM "USER";')

# вывод всех строк из таблицы
(cur.fetchall())

connection.commit()

cur.close()

connection.close()


bot = telebot.TeleBot(tk)


@bot.message_handler(commands=['start'])
def welcome_help(message):
    bot.send_message(message.chat.id, "Your'e started your bot")

# TODO:i need to fix 'connection'
#connection is lagged


@bot.message_handler(commands=['get_me'])
def get_message(message, connection):
    if message.chat.id == 'name':
        cursor = connection.cursor()
        cur.execute("SELECT * FROM USER_NAME  WHERE id = %s;", (2,))
        bot.send_message(message.chat.id, print(cur.fetchone().cursor))
        connection.commit()
        connection.close
    else:
        print('Please try again!')


if __name__ == '__main__':
    bot.infinity_polling(True)
