
import time

import psycopg2 as db
from psycopg2 import Error
# from uuid import uuid4
# import psycopg2.extras
import telebot
# from timeSoft_test import *

bot = telebot.TeleBot('1820948892:AAFrKqLgHq-4a4OqwMUz228BYVBbeht0oqY')

# print(MainUI().correct_login)
db_name = 'dt1vdgsvah47r'
db_user = 'ryxcgrjdgvrsxx'
db_password = '2e4d8cbc5b0f94259507584c6868f20ae0d4da79fdc618f6c2602d18045b2b61'
db_host = 'ec2-54-74-60-70.eu-west-1.compute.amazonaws.com'


connection = db.connect(database = db_name, user = db_user, password = db_password, host = db_host)
cursor = connection.cursor()
# db = DbLogic()


@bot.message_handler(commands=['start'])
def welcome_func(message):
    bot.send_message(message.chat.id,  'Если вы хотите зарегистрироваться то введите комманду логин /login')
    

# login_user = ''
# @bot.message_handler(commands=['login'])
# def message_about_name(login):
#     wlcm = bot.send_message(login.chat.id,"Hey!,  if u want to login please enter the name from app:'")
#     login_user = login.text()
#     bot.send_message(login.chat.id,f"it's your name {login_user.text}")

        

# password_user = ''
# @bot.message_handler(commands=['passsword'])
# def message_about_name(password):
#     wlcm = bot.send_message(password.chat.id,"Hey!,  if u want to login please enter the name from app:'")
#     login_user = password_user.text()
#     bot.send_message(password.chat.id,f"it's your name {login_user.text}")

# category_user = ''
# @bot.message_handler(commands=['category'])
# def message_about_name(category):
#     wlcm = bot.send_message(category.chat.id,"Hey!,  if u want to login please enter the name from app:'")
#     category_user = password_user.text()
#     bot.send_message(category.chat.id,f"it's your name {category_user.text}")


# activitie_user = ''
# @bot.message_handler(commands=['activities'])
# def message_about_name(activities):
#     wlcm = bot.send_message(activities.chat.id,"Hey!,  if u want to login please enter the name from app:'")
#     activities_user = password_user.text()
#     bot.send_message(activities.chat.id,f"it's your name {activities.text}")



if __name__ == 'main':
    bot.polling()