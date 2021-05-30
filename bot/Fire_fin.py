from typing import Text
import telebot
from telebot.apihelper import send_message
import psycopg2 as db
import time

from telebot.types import Message



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
def start_bot(message:Message):
    bot.send_message(message.chat.id,'Чтобы ввести имя нажмите команду "name"')

@bot.message_handler(commands=['name'])
def welcome_func(query:Message):
    message = query.text
    bot.send_message(query.chat.id,'Привет введите имя из приложения \'Timesoft\'')
    bot.register_next_step_handler(query,set_name)

def set_name(message):
    try:
        name = message.text
        check_user = cursor.execute(f"SELECT user_n_name FROM \"USER_NAME\" WHERE user_n_name = '{name}'")
        bot.send_message(check_user,message.chat.id,(f'Ваше имя {name}'))
    except Exception as e:
        bot.send_message(message.chat.id,f'column {name} does not exist')
    




    


# @bot.message_handler(commands=['log_in'])
# def input_log_name(message:Message):
#     name =  (message.chat.id,'Пожалуйста введите  имя зарегистрированое в "Timesoft":')
#     if f'{name}' in message.text:
#         bot.send_message(message,f'Your name is {name}')
#         return
#     # user_name = None
#     # name =  (message.chat.id,'Пожалуйста введите  имя зарегистрированое в "Timesoft":')
#     # if message.text == user_name:
#     #     print(user_name)
#     # check_user = cursor.execute(f'SELECT user_n_name FROM "USER_NAME" WHERE user_n_name = {message.chat.id}')
#     # c = cursor.fetchall()
#     # connection.commit()
#     # if  c == message.text:
#         bot.register_next_step_handler(bot.name,werivicate_name)
#     # else:
#     #print('Name is undefindet')
    


# def werivicate_name(message):
#         bot.send_message(message.chat.id,f'твое имя добавлено успешно message \'{message.text}\'')


# def input_login_name(message_id):

#     id = bot.send_message(message_id.chat.id,'Пожалуйста введите  пароль для приложения  "Time-soft":')
#     bot.register_next_step_handler(id,werivicate_parol)
#     add_sql = cursor.execute(f'SELECT user_p_pasword FROM "USER_PRIVATE" WHERE user_p_pasword = {message_id.text}')


#     c = cursor.fetchall()
#     connection.commit()
#     if c == message_id.text:
#         bot.register_next_step_handler( bot.name,werivicate_name)
#     else:
#         print('Name is undefindet')
    


# def werivicate_parol(message):
#     bot.send_message(message.chat.id,f'твой пароль потвержден успешно {message.text}')



if __name__ == '__main__': 
    while True:
        try:
            bot.infinity_polling(True)
        except Exception:
            time.sleep(15)