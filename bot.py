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
except Exception:
    TOKEN = config.get('Bot', 'bot_token_actvs')

general_commands = [
    '/edit_date',
    '/edit_event',
    '/edit_category',
    '/edit_time',
    '/edit_comment',
    '/delete_event',
    '/exit'
]

bot = telebot.TeleBot(TOKEN)

user_n_name = None
user_n_id = None
user_p_password = None
user_p_id = None
user_id = None
act_id = None
modifier = None
sorting = None
sent = []

connection = psycopg2.connect(database=config.get('PostgreSql', 'database'),
                              user=config.get('PostgreSql', 'user'),
                              password=config.get('PostgreSql', 'password'),
                              host=config.get('PostgreSql', 'host'))
cursor = connection.cursor()


def pre_check(message):
    global user_id
    global user_n_id
    cursor.execute(f"SELECT user_n_id FROM \"USER_NAME\" WHERE user_n_telegram = '{message.from_user.id}'")
    user_n_id = cursor.fetchall()
    if user_n_id:
        user_n_id = user_n_id[0][0]
        cursor.execute(f"SELECT user_id FROM \"USER\" WHERE user_n_id = '{user_n_id}'")
        user_id = cursor.fetchall()
        if user_id:
            user_id = user_id[0][0]


@bot.message_handler(commands=['start'])
def welcome_func(message):
    bot.send_message(message.chat.id, "Привет, для использования функционала бота войди в аккаунт с помощью комманды '/login'")


@bot.message_handler(commands=['login'])
def login_command(message):
    name_msg = bot.send_message(message.from_user.id, "Привет, введи своё имя.")
    bot.register_next_step_handler(name_msg, check_name)


@bot.message_handler(commands=['add'])
def login_command(message):
    date = datetime.now().strftime('%d.%m.%Y')
    name_msg = bot.send_message(message.from_user.id, f"Введи название, время, дату"
                                                      f"(для применения сегодняшеней даты [{date}] используй '-'),"
                                                      f"категорию и комментарий (необязательно) события.")
    bot.register_next_step_handler(name_msg, add_event)


def add_event(message):
    global user_id
    args = message.text.split(', ')
    if 4 <= len(args) <= 5:
        actl_name = args[1]
        act_time = args[2]
        act_date = args[3]
        cat_name = args[4]
        actl_name_check_len = InputCheck(actl_name).check_len()
        actl_name_check_incorrect_vals = InputCheck(actl_name).check_incorrect_vals()
        actl_name_check_spaces_tabs = InputCheck(actl_name).check_spaces_tabs()
        act_time_check = InputCheck(act_time).number_only()
        act_date_check = InputCheck(act_date).check_date()
        cat_name_check_len = InputCheck(cat_name).check_len()
        cat_name_check_incorrect_vals = InputCheck(cat_name).check_incorrect_vals()
        cat_name_check_spaces_tabs = InputCheck(cat_name).check_spaces_tabs()
        if len(args) == 5:
            act_comment = args[5]
            act_comment_check = InputCheck(act_comment)
        else:
            act_comment = 'NULL'
            act_comment_check = True
        entry = [actl_name_check_len, actl_name_check_incorrect_vals, actl_name_check_spaces_tabs, act_time_check, 
                 act_date_check, cat_name_check_len, cat_name_check_incorrect_vals, cat_name_check_spaces_tabs,
                 act_comment_check]
        failed = '\n'.join([x[1] for x in entry if type(x) == list])
        if not failed:
            try:
                cursor.execute(f"INSERT INTO \"ACTIVITY\" (user_id, actl_name, act_time, act_date, cat_name, act_comment) "
                               f"VALUES "
                               f"({user_id}, {actl_name}, {act_time}, {act_date}, {cat_name}, {act_comment})")
                connection.commit()
                bot.send_message(message.from_user.id, 'Событие было успешно добавлено.')
            except (Exception, DatabaseError):
                bot.send_message(message.from_user.id, 'Событие уже существует.')
        else:
            bot.send_message(message.from_user.id, 'Ошибка.\n' + failed)


def check_name(message):
    global user_n_id
    global user_p_id
    cursor.execute(f"SELECT user_n_id FROM \"USER_NAME\" WHERE user_n_name = '{message.text}'")
    user_n_id = cursor.fetchall()
    if user_n_id:
        user_n_id = user_n_id[0][0]
        cursor.execute(f"SELECT user_p_id FROM \"USER\" WHERE user_n_id = '{user_n_id}'")
        user_p_id = cursor.fetchall()
        if user_p_id:
            user_p_id = user_p_id[0][0]
        name_found_message = bot.send_message(message.from_user.id, 'Пользователь найден. Введите пароль.')
        bot.register_next_step_handler(name_found_message, check_password)
    else:
        bot.send_message(message.from_user.id, 'Зарегистрируйтесь в приложении для получения обновлений.')


def check_password(message):
    global user_id
    global user_p_password
    cursor.execute(f"SELECT user_p_password FROM \"USER_PRIVATE\" WHERE user_p_id = '{user_p_id}'")
    user_p_password = cursor.fetchall()
    if user_p_password:
        user_p_password = user_p_password[0][0]
        if message.text == user_p_password:
            cursor.execute(f"UPDATE \"USER_NAME\" SET user_n_telegram = '{message.from_user.id}' "
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


@bot.message_handler(commands=['display'])
def display_command(message):
    request_message = bot.send_message(message.from_user.id,
                                       'Выбери за сколько дней или между какими датами (раздели запятой) '
                                       'отобразить события.')
    bot.register_next_step_handler(request_message, display_by_date)


def display_by_date(message, sort_callback='date_sort'):
    global sent
    global sorting
    pre_check(message)
    if sort_callback == 'date_sort':
        sort_column = 'act_date ASC'
        sort_type = 'категориям'
    elif sort_callback == 'cat_sort':
        sort_column = 'cat_name ASC'
        sort_type = 'датам'
    else:
        return None
    if not sorting:
        sorting = message.text
    if sorting.isnumeric():
        n_days_ago_date = (datetime.now() - timedelta(days=int(sorting))).strftime('%Y-%m-%d')
        cursor.execute(f"SELECT * FROM \"ACTIVITY\" WHERE user_id = '{user_id}' AND act_date >= "
                       f"'{n_days_ago_date}'::date ORDER BY {sort_column} LIMIT 40")
        activities_type = ' за последние {} дней'.format(sorting)
    elif len(sorting.split(', ')) == 2:
        try:
            date_1 = datetime.strptime(sorting.split(', ')[0], '%d.%m.%Y').strftime('%Y-%m-%d')
            date_2 = datetime.strptime(sorting.split(', ')[1], '%d.%m.%Y').strftime('%Y-%m-%d')
            entry = [InputCheck(date_1).check_date(), InputCheck(date_2).check_date()]
            failed = [x[1] for x in entry if type(x) == list]
            if not failed:
                cursor.execute(f"SELECT * FROM \"ACTIVITY\" WHERE user_id = '{user_id}' AND act_date >= "
                               f"'{date_1}'::date AND act_date <= '{date_2}'::date ORDER BY {sort_column} LIMIT 40")
            else:
                bot.send_message(message.from_user.id, 'Ошибка.\nНеверный формат даты.')
            activities_type = ' с {0} по {1}'.format(sorting.split(', ')[0], sorting.split(', ')[1])
        except (Exception, DatabaseError):
            bot.send_message(message.from_user.id, 'Ошибка.\nНеверный формат даты.')
            activities_type = None
    else:
        seven_days_ago_date = (datetime.now() - timedelta(7)).strftime('%Y-%m-%d')
        cursor.execute(f"SELECT * FROM \"ACTIVITY\" WHERE user_id = '{user_id}' AND act_date >= "
                       f"'{seven_days_ago_date}'::date ORDER BY {sort_column} LIMIT 40")
        activities_type = ' за последние 7 дней'
    data = cursor.fetchall()
    data_list = [' '.join(['> ' + y[4].strftime('%d.%m.%Y'), str(y[2]), '({0})'.format(str(y[5])), str(y[3]),
                           'мин. /open_' + str(y[0])]) for y in data]
    data = '\n'.join(data_list)
    text = 'Это ваши активности{}:\n\n'.format(activities_type) + data
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Сортировать по " + sort_type, callback_data=sort_callback)
    markup = keyboard.add(button)
    if not sent:
        bot.send_message(message.from_user.id, text, reply_markup=markup)
        sent.append(message.chat.id)
        sent.append(message.message_id + 1)
    else:
        bot.edit_message_text(chat_id=sent[0], message_id=sent[1], text=text)
        bot.edit_message_reply_markup(chat_id=sent[0], message_id=sent[1], reply_markup=markup)


@bot.message_handler(func=lambda message: message.text and message.text.startswith('/open_'))
def edit_display_by_date(message):
    global act_id
    if not act_id:
        act_id = message.text[6:]
    cursor.execute(f"SELECT act_date, actl_name, cat_name, act_time, act_comment FROM \"ACTIVITY\" WHERE act_id = {act_id}")
    data = cursor.fetchall()
    act_date, actl_name, cat_name, act_time, act_comment = [str(x) for x in data[0]]
    options = 'Дата: ' + act_date + ' /edit_date\n' + \
              'Название: ' + actl_name + ' /edit_event\n' + \
              'Категория: ' + cat_name + ' /edit_category\n' + \
              'Время: ' + act_time + ' /edit_time\n' + \
              'Комментарий: ' + act_comment + ' /edit_comment\n' + \
              'Удалить событие /delete_event\n' + \
              'Выйти из режима просмотра /exit'
    edit_mode_message = bot.send_message(message.from_user.id, 'Внимание! Режим просмотра активности!\n\n' + options)
    bot.register_next_step_handler(edit_mode_message, choose_command)


@bot.message_handler(func=lambda message: message.text and message.text in general_commands)
def choose_command(message):
    global act_id
    global modifier
    try:
        if message.text == '/edit_date':
            event_message = bot.send_message(message.from_user.id, 'Введи дату.')
            modifier = 'act_date'
            bot.register_next_step_handler(event_message, process_command)
        elif message.text == '/edit_event':
            event_message = bot.send_message(message.from_user.id, 'Введи название.')
            modifier = 'actl_name'
            bot.register_next_step_handler(event_message, process_command)
        elif message.text == '/edit_category':
            event_message = bot.send_message(message.from_user.id, 'Введи категорию.')
            modifier = 'cat_name'
            bot.register_next_step_handler(event_message, process_command)
        elif message.text == '/edit_time':
            event_message = bot.send_message(message.from_user.id, 'Введи время.')
            modifier = 'act_time'
            bot.register_next_step_handler(event_message, process_command)
        elif message.text == '/edit_comment':
            event_message = bot.send_message(message.from_user.id, 'Введи комментарий.')
            modifier = 'act_comment'
            bot.register_next_step_handler(event_message, process_command)
        else:
            pass
    except (Exception, DatabaseError):
        display_by_date(message)
    if message.text == '/delete_event':
        bot.register_next_step_handler(message, process_command)
        cursor.execute(f"DELETE FROM \"ACTIVITY\" WHERE act_id = {act_id}")
        connection.commit()
        display_by_date(message)
    elif message.text == '/exit':
        display_by_date(message)
    else:
        pass


def process_command(message):
    global act_id
    global user_id
    global modifier
    pre_check(message)
    if not message.text.startswith('/open_'):
        if modifier == 'act_name':
            cursor.execute(f"UPDATE \"ACTIVITY\" SET {modifier} = '{message.text}' WHERE act_id = {act_id}")
        elif modifier == 'cat_name':
            cursor.execute(f"INSERT INTO \"CATEGORY\" (cat_name, user_id) VALUES ('{message.text}', {user_id})")
            cursor.execute(f"SELECT actl_id FROM \"ACTIVITY_LIST\" WHERE user_id = '{user_id}' LIMIT 1")
            actl_id = cursor.fetchall()
            if actl_id:
                actl_id = actl_id[0][0]
                cursor.execute(f"UPDATE \"ACTIVITY\" SET {modifier} = '{message.text}' WHERE act_id = {act_id}")
                cursor.execute(f"UPDATE \"ACTIVITY_LIST\" SET {modifier} = '{message.text}' WHERE actl_id = {actl_id}")
        else:
            cursor.execute(f"SELECT actl_id FROM \"ACTIVITY_LIST\" WHERE user_id = '{user_id}' LIMIT 1")
            actl_id = cursor.fetchall()
            if actl_id:
                actl_id = actl_id[0][0]
                cursor.execute(f"UPDATE \"ACTIVITY_LIST\" SET {modifier} = '{message.text}' WHERE actl_id = {actl_id}")
        connection.commit()
        edit_display_by_date(message)
    else:
        choose_command(message)


@bot.callback_query_handler(func=lambda callback: callback.data in ['date_sort', 'cat_sort'])
def callback_listener(callback):
    if callback.message:
        if callback.data == 'cat_sort':
            display_by_date(callback)
            bot.answer_callback_query(callback.id)
        elif callback.data == 'date_sort':
            display_by_date(callback, 'cat_sort')
            bot.answer_callback_query(callback.id)


@bot.message_handler(commands=[TOKEN])
def stop_bot():
    bot.stop_polling()


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
