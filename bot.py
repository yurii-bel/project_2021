import os

import telebot
import psycopg2

import configparser

from datetime import datetime, timedelta
from prettytable import from_db_cursor

from timeSoft_test import InputCheck


# get data from config.ini
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')


try:
    BOT_TOKEN = os.environ['BOT_TOKEN']
except Exception:
    TOKEN = config.get('Bot', 'bot_token_sasha')


# general Bot Telegram API class
bot = telebot.TeleBot(TOKEN)

# initialize connections between tables in db
user_n_name = None
user_n_id = None
user_p_password = None
user_p_id = None
user_id = None
act_id = None
modifier = None

# Initialize the connection to db
connection = psycopg2.connect(database=config.get('PostgreSql', 'database'),
                              user=config.get('PostgreSql', 'user'),
                              password=config.get('PostgreSql', 'password'),
                              host=config.get('PostgreSql', 'host'))
cursor = connection.cursor()


def pre_check(message):
    global user_id
    cursor.execute(f"SELECT user_n_id FROM \"USER_NAME\" WHERE user_n_telegram = '{message.from_user.id}'")
    user_n_id = cursor.fetchall()
    if user_n_id:
        user_n_id = user_n_id[0][0]
        cursor.execute(f"SELECT user_id FROM \"USER\" WHERE user_n_id = '{user_n_id}'")
        user_id = cursor.fetchall()
        if user_id:
            user_id = user_id[0][0]


# start command handler
@bot.message_handler(commands=['start'])
def welcome_func(message):
    bot.send_message(message.chat.id, "Привет, для использования функционала бота войди в аккаунт с помощью комманды '/login'")


# login command handler
@bot.message_handler(commands=['login'])
def login_command(message):
    name_msg = bot.send_message(message.from_user.id, "Привет, введи своё имя.")
    bot.register_next_step_handler(name_msg, check_name)


# checks if user is in the chat
def check_name(message):
    global user_n_id
    global user_p_id
    # getting user_n_id from USER_NAME
    cursor.execute(f"SELECT user_n_id FROM \"USER_NAME\" WHERE user_n_name = '{message.text}'")
    user_n_id = cursor.fetchall()
    if user_n_id:
        user_n_id = user_n_id[0][0]
        # getting user_p_id from USER
        cursor.execute(f"SELECT user_p_id FROM \"USER\" WHERE user_n_id = '{user_n_id}'")
        user_p_id = cursor.fetchall()
        if user_p_id:
            user_p_id = user_p_id[0][0]
        name_found_message = bot.send_message(message.from_user.id, 'Пользователь найден. Введите пароль.')
        bot.register_next_step_handler(name_found_message, check_password)
    else:
        bot.send_message(message.from_user.id, 'Зарегистрируйтесь в приложении для получения обновлений.')


# checks if the entered password is equal to the entered one
def check_password(message):
    global user_id
    # getting user_p_password from USER_PRIVATE
    cursor.execute(f"SELECT user_p_password FROM \"USER_PRIVATE\" WHERE user_p_id = '{user_p_id}'")
    user_p_password = cursor.fetchall()
    if user_p_password:
        user_p_password = user_p_password[0][0]
        if message.text == user_p_password:
            # setting user_n_telegram from USER_NAME
            cursor.execute(f"UPDATE \"USER_NAME\" SET user_n_telegram = '{message.from_user.id}' " \
                           f"WHERE user_n_id = '{user_n_id}'")
            connection.commit()
            bot.send_message(message.from_user.id, 'Успешно, вход в аккаунт..')
            cursor.execute(f"SELECT user_id FROM \"USER\" WHERE user_n_id = '{user_n_id}'")
            user_id = cursor.fetchall()
            if user_id:
                user_id = user_id[0][0]
        elif message.text == '/login':
            login_command(message)
        else:
            unsuccessful_msg = bot.send_message(message.from_user.id, 'Неверный пароль, повторите попытку..')
            bot.register_next_step_handler(unsuccessful_msg, check_password)


# display command handler
@bot.message_handler(commands=['display'])
def display_by_date(message):
    global data
    pre_check(message)
    seven_days_ago_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    cursor.execute(f"SELECT * FROM \"ACTIVITY\" WHERE user_id = '{user_id}' AND act_date > '{seven_days_ago_date}'::date ORDER BY act_date, act_id")
    data = cursor.fetchall()
    data_list = [' '.join(['> ' + y[4].strftime('%Y.%m.%d'), str(y[2]), '({0})'.format(str(y[5])), str(y[3]), 'мин. /open_' + str(y[0])]) for y in data]
    data = '\n'.join(data_list)
    bot.send_message(message.from_user.id, 'Это ваши активности за последние 7 дней:\n\n' + data)


@bot.message_handler(func=lambda message: message.text and message.text.startswith('/open_'))
def edit_display_by_date(message):
    global act_id
    act_id = message.text[6:]
    cursor.execute(f"SELECT act_date, cat_name, actl_name, act_time, act_comment FROM \"ACTIVITY\" WHERE act_id = {act_id}")
    data = cursor.fetchall()
    act_date, cat_name, actl_name, act_time, act_comment = [str(x) for x in data[0]]
    options = 'Дата: ' + act_date + ' /edit_date\n' + \
              'Категория: ' + cat_name + ' /edit_category\n' + \
              'Название: ' + actl_name + ' /edit_event\n' + \
              'Время: ' + act_time + ' /edit_time\n' + \
              'Комментарий: ' + act_comment + ' /edit_comment\n' + \
              'Удалить событие /delete_event\n' + \
              'Выйти из режима просмотра /exit'
    edit_mode_message = bot.send_message(message.from_user.id, 'Внимание! Режим просмотра активности!\n\n' + options)
    bot.register_next_step_handler(edit_mode_message, choose_command)


# TODO: need to fix that ASAP
def choose_command(message):
    global act_id
    global modifier
    try:
        if message.text == '/edit_date':
            modifier = 'act_date'
            event_message = bot.send_message(message.from_user.id, 'Введи дату.')
        elif message.text == '/edit_event':
            modifier = 'actl_name'
            event_message = bot.send_message(message.from_user.id, 'Введи категорию.')
        elif message.text == '/edit_category':
            modifier = 'cat_name'
            event_message = bot.send_message(message.from_user.id, 'Введи название.')
        elif message.text == '/edit_time':
            modifier = 'act_time'
            event_message = bot.send_message(message.from_user.id, 'Введи время.')
        elif message.text == '/edit_comment':
            modifier = 'act_comment'
            event_message = bot.send_message(message.from_user.id, 'Введи комментарий.')
        bot.register_next_step_handler(event_message, process_command)
    except Exception:
        display_by_date(message)
    try:
        if message.text == '/delete_event':
            cursor.execute(f"DELETE FROM \"ACTIVITY\" WHERE act_id = {act_id}")
            connection.commit()
            bot.register_next_step_handler(message, process_command)
            display_by_date(message)
        elif message.text == '/exit':
            display_by_date(message)
    except Exception:
        display_by_date(message)
    finally:
        act_id = None
        modifier = None
        bot.clear_step_handler_by_chat_id(message.chat.id)


def process_command(message):
    global act_id
    global modifier
    cursor.execute(f"UPDATE \"ACTIVITY\" SET {modifier} = {message.text} WHERE act_id = {act_id}")
    connection.commit()
    edit_display_by_date(message)


@bot.message_handler(commands=[TOKEN])
def stop_bot():
    bot.stop_polling()


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
