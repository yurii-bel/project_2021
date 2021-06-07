import os

import telebot
import psycopg2

# import configparser

# from datetime import datetime, timedelta
# from prettytable import from_db_cursor

# from timeSoft_test import InputCheck


# get data from config.ini
# config = configparser.ConfigParser()
# config.read('config.ini', encoding='utf-8-sig')


# try:
#     BOT_TOKEN = os.environ['BOT_TOKEN']
# except Exception:
#     TOKEN = config.get('Bot', 'bot_token_sasha')

token = '1820948892:AAFrKqLgHq-4a4OqwMUz228BYVBbeht0oqY'

# general Bot Telegram API class
bot = telebot.TeleBot(token)


@bot.message_handler(commands= ['start'])
def start_bot(message):
    bot.send_message(message.chat.id, 'Привет если вы хотите авторизировать вашего бота введите команду  /login')


