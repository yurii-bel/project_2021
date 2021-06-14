import telebot
import psycopg2

import os

from psycopg2 import DatabaseError

import configparser

from datetime import datetime, timedelta
from telebot import types

from timeSoft_test import InputCheck


config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')

try:
    BOT_TOKEN = os.environ['BOT_TOKEN']
    DATABASE_URL = os.environ['DATABASE_URL']
    connection = psycopg2.connect(DATABASE_URL)
except KeyError:
    BOT_TOKEN = config.get('Bot', 'bot_token_sasha')
    connection = psycopg2.connect(database=config.get('PostgreSql', 'database'),
                                  user=config.get('PostgreSql', 'user'),
                                  password=config.get('PostgreSql', 'password'),
                                  host=config.get('PostgreSql', 'host'))

bot = telebot.TeleBot(BOT_TOKEN)

cursor = connection.cursor()

user_n_name = None
user_n_id = None
user_p_password = None
user_p_id = None
user_id = None
act_id = None
modifier = None
sorting = None
change = False


# def pre_check(message):
#     global user_n_id
#     global user_id
#     cursor.execute(f"SELECT user_n_id FROM \"USER_NAME\" WHERE user_n_telegram = '{message.from_user.id}'")
#     user_n_id = cursor.fetchall()
#     if user_n_id:
#         user_n_id = user_n_id[0][0]
#         cursor.execute(f"SELECT user_id FROM \"USER\" WHERE user_n_id = '{user_n_id}'")
#         user_id = cursor.fetchall()
#         if user_id:
#             user_id = user_id[0][0]


@bot.message_handler(commands=['start'])
def hello_user(message):
    bot.send_message(message.chat.id,'Добрый день , я помошник бот для приложения ТаймСофт пожалуйста если\
         вы хотите пользоваться мной введите команду \'/login\'')




@bot.message_handler(commands=['login'])
def login_me(message):
    user_message = bot.send_message(message.from_user.id, 'Если вы зарегистрированы в приложениии\
         ТаймСофт введите свое имя: ')
    bot.register_next_step_handler(message,name_of_user)

def name_of_user(message):
    global user_n_name
    global user_n_id
    cursor.execute(f"SELECT user_n_id FROM \"USER_NAME\" WHERE user_n_name = '{message.text}' ")
    connection.commit()
    user_n_id = cursor.fetchall()
    if user_n_id:
        user_n_id = user_n_id[0][0]
        bot.send_message(message.chat.id,'Отлично имя верное теперь введите пароль: ')
        bot.register_next_step_handler(message,password_of_user)
    else: bot.send_message(message.chat.id,'Такого пароля не существует пожалуйста зарегистрируйтесь в приложениии')

def password_of_user(message):
    global user_p_password
    global user_p_id
    cursor.execute(f"SELECT user_p_id FROM \"USER_PRIVATE\" WHERE user_p_password = '{message.text}'")
    connection.commit()
    user_p_id = cursor.fetchall()
    if user_p_id:
        user_p_id = user_p_id[0][0]
        bot.register_next_step_handler(message,succsessful_registration)
        print(user_p_id)
    


def succsessful_registration(message):
    global user_p_id
    global user_id
    cursor.execute(f"UPDATE \"USER_NAME\" WHERE user_p_id = '{user_p_id}' ")
    connection.commit()
    if user_id:
        user_id = user_id[0][0]
        bot.send_message(message.chat_id, '\Yor\'re registrations had been succsessful!')
        print(user_id)
    else: bot.send_message(message.chat.id,'Такого пароля не существует пожалуйста зарегистрируйтесь в приложениии')
    




if __name__ == '__main__':
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            print(e)
