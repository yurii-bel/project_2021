import telebot
from telebot.types import User
import psycopg2 as db
tk = '1891194594:AAGDaHHTuZv5mDBIV8Q4Sjd7xU1RPPry0ns'


class TelegramBot:

    database = 'dt1vdgsvah47r'
    user = 'ryxcgrjdgvrsxx'
    password = '2e4d8cbc5b0f94259507584c6868f20ae0d4da79fdc618f6c2602d18045b2b61'
    host = 'ec2-54-74-60-70.eu-west-1.compute.amazonaws.com'

    def __init__(self):
        self.connection = db.connect(database=self.database,
                                     user=self.user,
                                     password=self.password,
                                     host=self.host)

        self.cursor = self.connection.cursor()

        self.correct_login_info = False

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
    telegrambot = TelegramBot

    bot.telegrambot.infinity_polling(True)
