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

@bot.message_handler(command = 'categories')
def add_action(message):
    name = message.from_user.id
    cursor.execute("""SELECT (user_id,cat) TABLE IF NOT EXIST CATEGORY(
        user_id INTEGER
        cat_name STRING
        )""")

    user_abilities = [message.chat.user_id, message.chat.cat_name]
    cursor.execute("INSERT INTO CATEGORY VALUES(%s,%s);",user_abilities)
    db.connect.commit()


if __name__ == '__main__':
 while True:
    try:
        bot.infinity_polling(True)
    except Exception:
        time.sleep(15)

