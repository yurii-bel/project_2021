import telebot
from telebot.types import User
import psycopg2 as db
import time
tk = '1891194594:AAGDaHHTuZv5mDBIV8Q4Sjd7xU1RPPry0ns'




db_name = 'dt1vdgsvah47r'
db_user = 'ryxcgrjdgvrsxx'
db_password = '2e4d8cbc5b0f94259507584c6868f20ae0d4da79fdc618f6c2602d18045b2b61'
db_host = 'ec2-54-74-60-70.eu-west-1.compute.amazonaws.com'


connection = db.connect(database = db_name, user = db_user, password = db_password, host = db_host)

cursor = connection.cursor()
correct_login_info = False
bot = telebot.TeleBot(tk)

def  find_at(msg):
    for text in msg:
        if '@' in text:
            return text



@bot.message_handler(func = lambda msg: msg.text is not None and  '@'  in msg.text)
def at_answer(message):
    text = message.text.split()
    at_text = find_at(text)

    bot.reply_to(message, 'https://instagram.com{}'.format(at_text))



@bot.message_handler(commands=['start'])
def welcome_help(message):
    bot.send_message(message.chat.id, "Your'e started your bot")


# #connection is lagged

@bot.message_handler(commands=['get_me'])
def get_message(message):
    name = message.from_user.id
    cursor.execute('S'
        #add values
    bot.send_message(message.chat.id,f"it's your name {name}") #print(cursor.fetchone().cursor))
    connection.commit()
    connection.close





if __name__ == '__main__':
 while True:
    try:
        bot.infinity_polling(True)
    except Exception:
        time.sleep(15)

