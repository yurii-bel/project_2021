from typing import Text
import telebot
from telebot.apihelper import send_message
from telebot.types import Message, User
import psycopg2 as db
from psycopg2 import sql
import time



tk = '1891194594:AAGDaHHTuZv5mDBIV8Q4Sjd7xU1RPPry0ns'




db_name = 'dt1vdgsvah47r'
db_user = 'ryxcgrjdgvrsxx'
db_password = '2e4d8cbc5b0f94259507584c6868f20ae0d4da79fdc618f6c2602d18045b2b61'
db_host = 'ec2-54-74-60-70.eu-west-1.compute.amazonaws.com'


connection = db.connect(database = db_name, user = db_user, password = db_password, host = db_host)

cursor =   connection.cursor()
correct_login_info = False
bot = telebot.TeleBot(tk)





@bot.message_handler(commands=['start'])
def welcome_func(message):
    name = bot.send_message(message.chat.id,"Привет если вы хотите войти введите команы '/login'  для потверждения имени, '/пароль для потверждения пароля")
        



@bot.message_handler(commands=['login'])
def input_log_name(message):
    name =  (message.chat.id,'Пожалуйста введите  имя зарегистрированое в "Timesoft":')
    check_user = cursor.execute(f'SELECT user_n_name FROM "USER_NAME" WHERE user_n_name = {message.}')
    print(message)
    c = cursor.fetchall()
    connection.commit()
    # if  c == message.text:
    bot.register_next_step_handler(bot.name,werivicate_name)
    print(check_user)
    # else:
    #     print('Name is undefindet')
    


def werivicate_name(message):
        bot.send_message(message.chat.id,f'твое имя добавлено успешно message \'{message.text}\'')


def input_log_name(message_id):

    id = bot.send_message(message_id.chat.id,'Пожалуйста введите  пароль для приложения  "Time-soft":')
    bot.register_next_step_handler(id,werivicate_parol)
    add_sql = cursor.execute(f'SELECT user_p_pasword FROM "USER_PRIVATE" WHERE user_p_pasword = {message_id.text}')


    c = cursor.fetchall()
    connection.commit()
    if c == message_id.text:
        bot.register_next_step_handler( bot.name,werivicate_name)
    else:
        print('Name is undefindet')
    


def werivicate_parol(message):
    bot.send_message(message.chat.id,f'твой пароль потвержден успешно {message.text}')



if __name__ == '__main__': 
    while True:
        try:
            bot.infinity_polling(True)
        except Exception:
            time.sleep(15)