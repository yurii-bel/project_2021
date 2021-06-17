import os
import telebot
import psycopg2
import configparser

from psycopg2 import DatabaseError
from datetime import datetime
from telebot import types
from timeSoft_test import InputCheck


try:
    BOT_TOKEN = os.environ['BOT_TOKEN']
    DATABASE_URL = os.environ['DATABASE_URL']
    connection = psycopg2.connect(DATABASE_URL)
except KeyError:
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8-sig')
    BOT_TOKEN = config.get('Bot', 'bot_token_timesoft')
    connection = psycopg2.connect(config.get('PostgreSql', 'DATABASE_URL'))

bot = telebot.TeleBot(BOT_TOKEN)

cursor = connection.cursor()

general_commands = [
    '/start',
    '/login',
    '/display',
    '/add'
]
specific_commands = [
    '/edit_date',
    '/edit_event',
    '/edit_category',
    '/edit_time',
    '/edit_comment',
    '/delete_event',
    '/exit_event'
]
commands = general_commands + specific_commands

users_data = {}


@bot.message_handler(commands=['start'])
def start_command(message):
    remove_act_id(message)
    bot.send_message(
        message.chat.id, "Привет, для использования функционала бота войди в аккаунт с помощью комманды /login")


@bot.message_handler(commands=['login'])
def login_command(message):
    remove_act_id(message)
    login_message = bot.send_message(message.chat.id, "Введи своё имя.")
    bot.register_next_step_handler(login_message, check_login)


@bot.message_handler(commands=['display'])
def display_command(message):
    remove_act_id(message)
    # Check whether user is logged in
    if 'logged_in_' + str(message.from_user.id) in users_data:
        # Get current date in a certain format
        date = datetime.now().strftime('%d\\.%m\\.%Y')
        display_message = bot.send_message(message.chat.id, f'Какие даты отобразить?\n\n'
                                           f'*Пример:*\n'
                                           f'*\\-* — все события за сегодня \\(*{date}*\\)\\.\n'
                                           f'*7* — за последние 7 дней\\.\n'
                                           f'*01\\.06\\.2021* — конкретную дату\\.\n'
                                           f'*01\\.01\\.2020, 01\\.01\\.2021* — все события между датами\\.',
                                           parse_mode='MarkdownV2')
        bot.register_next_step_handler(display_message, display_events)
    else:
        bot.send_message(
            message.chat.id, 'Войдите в аккаунт с помощью комманды /login для использования этой функции.')


@bot.message_handler(commands=['add'])
def add_command(message):
    remove_act_id(message)
    # Check whether user is logged in
    if 'logged_in_' + str(message.from_user.id) in users_data:
        # Get current date in a certain format
        date = datetime.now().strftime('%d\\.%m\\.%Y')
        add_message = bot.send_message(message.chat.id, f'Добавляем новое событие\\.\n\n'
                                       f'*Необходимо ввести:*\n'
                                       f'Название события, затраченное время, дату события, категорию, комментарий '
                                       f'\\(необязательно\\)\\.\n\nОбратите внимание, для ввода даты можно использовать '
                                       f'следующие варианты ввода:\n*\\-* — показать все события за сегодня \\(*{date}*\\)\\.\n'
                                       f'*16\\.06\\.2021* — показать конкретную дату\\.\n\n'
                                       f'*Например*:\n'
                                       f'Гулял, 42, 06\\.06\\.2021, Отдых, В парке\n'
                                       f'Смотрел фильм, 153, \\-, Отдых, Король лев\n'
                                       f'Готовил еду, 45, \\-, Быт\n',
                                       parse_mode='MarkdownV2')
        bot.register_next_step_handler(add_message, add_event)
    else:
        bot.send_message(
            message.chat.id, 'Войдите в аккаунт с помощью комманды /login для использования этой функции.')


def check_login(message):
    # Solve functions overlapping
    if message.text == '/start':
        return start_command(message)
    elif message.text == '/login':
        return login_command(message)
    elif message.text == '/display':
        return display_command(message)
    elif message.text.startswith('/open_') and len(message.text) > 6:
        return edit_event(message)
    elif message.text == '/add':
        return add_command(message)
    checks = [
        InputCheck(message.text).check_incorrect_vals()
    ]
    failed = []
    for x in checks:
        if type(x) is list:
            failed.append(x[1])
    if failed:
        failed = ' '.join(list(set(failed)))
        error_message = bot.send_message(
            message.chat.id, 'Произошла ошибка. ' + failed)
        return bot.register_next_step_handler(error_message, check_login)
    # Fetch user_n_id with text entered by the user
    cursor.execute(
        f'SELECT user_n_id FROM "USER_NAME" WHERE user_n_name = \'{message.text}\'')
    data = cursor.fetchall()
    if data:
        user_n_id = data[0][0]
        # Save user_n_id to the global dict
        users_data['user_n_id_' + str(message.from_user.id)] = user_n_id
        # Got login
        password_message = bot.send_message(message.chat.id, 'Введи пароль.')
        bot.register_next_step_handler(password_message, check_password)
    else:
        # User doesn't exist, tell the user to register
        error_message = bot.send_message(message.chat.id, 'Не удалось найти пользователя. '
                                                          'Повтори попытку или зарегистрируйся в приложении.')
        return bot.register_next_step_handler(error_message, check_login)


def check_password(message):
    # Solve functions overlapping
    if message.text == '/start':
        return start_command(message)
    elif message.text == '/login':
        return login_command(message)
    elif message.text == '/display':
        return display_command(message)
    elif message.text.startswith('/open_') and len(message.text) > 6:
        return edit_event(message)
    elif message.text == '/add':
        return add_command(message)
    # Get user_n_id saved to the global dict
    try:
        user_n_id = users_data['user_n_id_' + str(message.from_user.id)]
    except KeyError:
        return bot.send_message(message.chat.id, 'Произошла ошибка.')
    checks = [
        InputCheck(message.text).check_incorrect_vals()
    ]
    failed = []
    for x in checks:
        if type(x) is list:
            failed.append(x[1])
    if failed:
        failed = ' '.join(list(set(failed)))
        error_message = bot.send_message(
            message.chat.id, 'Произошла ошибка. ' + failed)
        return bot.register_next_step_handler(error_message, check_password)
    # Fetch user_p_id with user_n_id we got from the check_login
    cursor.execute(
        f'SELECT user_p_id, user_id FROM "USER" WHERE user_n_id = \'{user_n_id}\'')
    data = cursor.fetchall()
    if data:
        user_p_id = data[0][0]
        user_id = data[0][1]
        # Save user_id to the global dict
        users_data['user_id_' + str(message.from_user.id)] = user_id
        # Fetch user_p_password with user_p_id we got from the last step
        cursor.execute(
            f'SELECT user_p_password FROM "USER_PRIVATE" WHERE user_p_id = \'{user_p_id}\'')
        data = cursor.fetchall()
        if data:
            user_p_password = data[0][0]
            # Check entered password
            if message.text == user_p_password:
                # Save logged state to the global dict
                users_data['logged_in_' + str(message.from_user.id)] = True
                cursor.execute(f'UPDATE "USER_NAME" SET user_n_telegram = \'{message.from_user.id}\''
                               f'WHERE user_n_id = \'{user_n_id}\'')
                connection.commit()
                bot.send_message(message.chat.id, 'Успешно.\nДля отображения событий испоьзуй комманду /display\n'
                                                  'Для добавления нового события используй комманду /add')
            else:
                error_message = bot.send_message(
                    message.chat.id, 'Неверный пароль. Повтори попытку.')
                # Reenter the same function if password is incorrect
                bot.register_next_step_handler(
                    error_message, check_password)
        else:
            # If couldn't get user_p_password
            bot.send_message(message.chat.id, 'Произошла ошибка.')
    else:
        # If couldn't get user_p_id
        bot.send_message(message.chat.id, 'Произошла ошибка.')


def display_events(message, sort_callback='date_sort', edit=False, refresh=False):
    if not (edit or refresh):
        # Solve functions overlapping
        if message.text == '/start':
            return start_command(message)
        elif message.text == '/login':
            return login_command(message)
        elif message.text == '/display':
            return display_command(message)
        elif message.text.startswith('/open_') and len(message.text) > 6:
            return edit_event(message)
        elif message.text == '/add':
            return add_command(message)
    # Define sorting vars needed for activities sorting and sorting button name
    if sort_callback == 'cat_sort':
        sort_column = 'cat_name'
        sort_type = 'датам'
    else:
        sort_column = 'act_date'
        sort_type = 'категориям'
    # Get user_id saved to the global dict
    try:
        user_id = users_data['user_id_' + str(message.from_user.id)]
    except KeyError:
        return bot.send_message(message.chat.id, 'Произошла ошибка.')
    # Handle sorting button click
    if edit or refresh:
        if edit:
            try:
                txt = users_data['user_entry_' + str(message.from_user.id)]
            except KeyError:
                return bot.send_message(message.chat.id, 'Произошла ошибка.')
        else:
            try:
                txt = users_data['user_entry_' + str(message.from_user.id)]
            except KeyError:
                return bot.answer_callback_query(message.id)
    else:
        txt = message.text
    checks = [
        InputCheck(txt).check_date() if txt != '-' else True,
        InputCheck(txt).check_incorrect_vals()
    ]
    failed = []
    for x in checks:
        if type(x) is list:
            failed.append(x[1])
    if failed:
        failed = ' '.join(list(set(failed)))
        error_message = bot.send_message(
            message.chat.id, 'Произошла ошибка. ' + failed)
        return bot.register_next_step_handler(error_message, display_events)
    elif txt.isdigit():
        users_data['user_entry_' + str(message.from_user.id)] = txt
        cursor.execute(f'SELECT * FROM "ACTIVITY" WHERE user_id = \'{user_id}\' AND act_date >= '
                       f'(NOW()::date - \'{txt} days\'::interval) ORDER BY {sort_column} LIMIT 50')
        if int(txt) in range(11, 20):
            days = 'дней'
        elif int(txt[-1]) == 1:
            days = 'день'
        elif int(txt[-1]) in range(2, 5):
            days = 'дня'
        else:
            days = 'дней'
        activities_type = f'за последние {txt} {days}'
    elif len(txt.split(', ')) == 1:
        if txt == '-':
            date = datetime.now()
            txt = date.strftime('%d.%m.%Y')
        else:
            date = datetime.strptime(txt, '%d.%m.%Y').strftime('%Y-%m-%d')
        users_data['user_entry_' + str(message.from_user.id)] = txt
        cursor.execute(f'SELECT * FROM "ACTIVITY" WHERE user_id = \'{user_id}\' AND act_date = \'{date}\'::date '
                       f'ORDER BY {sort_column} LIMIT 50')
        activities_type = f'за {txt}'
    elif len(txt.split(', ')) == 2:
        users_data['user_entry_' + str(message.from_user.id)] = txt
        date_1, date_2 = txt.split(', ')
        date_1_formatted, date_2_formatted = [
            datetime.strptime(x, '%d.%m.%Y') for x in [date_1, date_2]]
        date_1_sorted, date_2_sorted = sorted(
            [date_1_formatted, date_2_formatted])
        date_1_cleared, date_2_cleared = [x.strftime(
            '%Y-%m-%d') for x in [date_1_sorted, date_2_sorted]]
        sort_column += ' ASC' if date_1_formatted == date_1_sorted else ' DESC'
        cursor.execute(f'SELECT * FROM "ACTIVITY" WHERE user_id = \'{user_id}\' AND act_date BETWEEN '
                       f'\'{date_1_cleared}\'::date AND \'{date_2_cleared}\'::date ORDER BY {sort_column} LIMIT 50')
        activities_type = 'с {0} по {1}'.format(date_1, date_2)
    else:
        error_message = bot.send_message(
            message.chat.id, 'Произошла ошибка. Неверный формат.')
        return bot.register_next_step_handler(error_message, display_events)
    data = cursor.fetchall()
    if data:
        # Make data readable
        activities_list = []
        for y in data:
            pointer = '> '
            date = y[4].strftime('%d.%m.%Y')
            name = str(y[2])
            category = str(y[5])
            time = f'({str(y[3])})' + ' мин.'
            link = '/open_' + str(y[0])
            vals = ' '.join([pointer, date, name, category, time, link])
            activities_list.append(vals)
        activities = '\n'.join(activities_list)
        text = f'Это ваши активности {activities_type}:\n\n' + activities
        # Add sorting button if the number of activities exceeds 5
        if len(activities_list) > 5:
            # Define sorting button
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(
                "Сортировать по " + sort_type, callback_data=sort_callback)
            markup = keyboard.add(button)
        else:
            markup = None
    else:
        text = 'Активности отсутствуют.'
        markup = None
    # Handle sorting button click
    if edit:
        # Accessing message attribute of CallbackQuery
        message = message.message
        # Edit message with resorting events oppositely and replacing the button to the opposite one
        bot.edit_message_text(chat_id=message.chat.id,
                              message_id=message.message_id, text=text)
        bot.edit_message_reply_markup(
            chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup)
        return
    else:
        bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text.startswith('/open_'))
def edit_event(message):
    # Check whether user is logged in
    if 'logged_in_' + str(message.from_user.id) in users_data:
        # If editing mode is being called by the command, set act_id to actual event's id
        if message.text.startswith('/open_'):
            act_id = message.text[6:]
        else:
            try:
                act_id = users_data['act_id_' + str(message.from_user.id)]
            except KeyError:
                act_id = message.text[6:]
        # Check whether event is available for the user
        try:
            user_id = users_data['user_id_' + str(message.from_user.id)]
            cursor.execute(
                f'SELECT act_id FROM "ACTIVITY" where user_id = {user_id}')
            act_ids = cursor.fetchall()
            act_ids = [str(x[0]) for x in act_ids]
            if act_id not in act_ids:
                remove_act_id(message)
                return bot.send_message(message.chat.id, 'Событие недоступно.')
        except (KeyError, DatabaseError):
            return bot.send_message(message.chat.id, 'Произошла ошибка.')
        # Save act_id to the global dict
        users_data['act_id_' + str(message.from_user.id)] = act_id
        # Fetch event's data
        cursor.execute(f'SELECT act_date, actl_name, cat_name, act_time, act_comment '
                       f'FROM "ACTIVITY" WHERE act_id = {act_id}')
        data = cursor.fetchall()
        if data:
            act_date, actl_name, cat_name, act_time, act_comment = data[0]
        else:
            return bot.send_message(message.chat.id, 'Произошла ошибка.')
        # Format data
        act_date = datetime.combine(
            act_date, datetime.min.time()).strftime('%d.%m.%Y')
        act_comment = act_comment if act_comment else '—'
        actl_name, cat_name, act_time, act_comment = [
            str(x) for x in [actl_name, cat_name, act_time, act_comment]]
        options = 'Дата: ' + act_date + ' /edit_date\n' + \
                  'Название: ' + actl_name + ' /edit_event\n' + \
                  'Категория: ' + cat_name + ' /edit_category\n' + \
                  'Время: ' + act_time + ' мин. /edit_time\n' + \
                  'Комментарий: ' + act_comment + ' /edit_comment\n' + \
                  'Удалить событие /delete_event\n' + \
                  'Выйти из режима просмотра /exit_event'
        bot.send_message(message.chat.id, f'Событие {act_id}!\n\n' + options)
    else:
        bot.send_message(
            message.chat.id, 'Войдите в аккаунт с помощью комманды /login для использования этой функции.')


@bot.message_handler(func=lambda message: message.text in specific_commands)
def choose_action(message):
    # Check whether user is logged in
    if 'logged_in_' + str(message.from_user.id) in users_data:
        # Handle specific commands clicks
        if message.text == '/edit_date':
            event_message = bot.send_message(message.chat.id, 'Введи дату.')
            users_data['modifier_' + str(message.from_user.id)] = 'act_date'
        elif message.text == '/edit_event':
            event_message = bot.send_message(
                message.chat.id, 'Введи название.')
            users_data['modifier_' + str(message.from_user.id)] = 'actl_name'
        elif message.text == '/edit_category':
            event_message = bot.send_message(
                message.chat.id, 'Введи категорию.')
            users_data['modifier_' + str(message.from_user.id)] = 'cat_name'
        elif message.text == '/edit_time':
            event_message = bot.send_message(message.chat.id, 'Введи время.')
            users_data['modifier_' + str(message.from_user.id)] = 'act_time'
        elif message.text == '/edit_comment':
            event_message = bot.send_message(
                message.chat.id, 'Введи комментарий.')
            users_data['modifier_' + str(message.from_user.id)] = 'act_comment'
        elif message.text == '/delete_event':
            # Try and delete the event
            try:
                # Get act_id saved to the global dict
                try:
                    act_id = users_data['act_id_' + str(message.from_user.id)]
                except KeyError:
                    return bot.send_message(message.chat.id, 'Произошла ошибка.')
                cursor.execute(
                    f'DELETE FROM "ACTIVITY" WHERE act_id = {act_id}')
                connection.commit()
            except DatabaseError:
                bot.send_message(message.chat.id, 'Произошла ошибка.')
            remove_act_id(message)
            return display_events(message, refresh=True)
        else:
            remove_act_id(message)
            return display_events(message, refresh=True)
        bot.register_next_step_handler(event_message, process_action)
    else:
        bot.send_message(
            message.chat.id, 'Войдите в аккаунт с помощью комманды /login для использования этой функции.')


def process_action(message):
    # Solve functions overlapping
    if message.text == '/start':
        return start_command(message)
    elif message.text == '/login':
        return login_command(message)
    elif message.text == '/display':
        return display_command(message)
    elif message.text.startswith('/open_') and len(message.text) > 6:
        return edit_event(message)
    elif message.text == '/add':
        return add_command(message)
    checks = [
        InputCheck(message.text).check_incorrect_vals()
    ]
    failed = []
    for x in checks:
        if type(x) is list:
            failed.append(x[1])
    if failed:
        failed = ' '.join(list(set(failed)))
        error_message = bot.send_message(
            message.chat.id, 'Произошла ошибка. ' + failed)
        return bot.register_next_step_handler(error_message, process_action)
    # Get user_id, modifier, act_id saved to the global dict
    try:
        user_id = users_data['user_id_' + str(message.from_user.id)]
        modifier = users_data['modifier_' + str(message.from_user.id)]
        act_id = users_data['act_id_' + str(message.from_user.id)]
    except KeyError:
        return bot.send_message(message.chat.id, 'Произошла ошибка.')
    # Handle checks for different modifiers
    if modifier == 'act_date':
        checks = [
            InputCheck(message.text).check_date()
        ]
    elif modifier == 'actl_name':
        checks = [
            InputCheck(message.text).check_len(),
            InputCheck(message.text).check_incorrect_vals()
        ]
    elif modifier == 'cat_name':
        checks = [
            InputCheck(message.text).check_len(),
            InputCheck(message.text).check_incorrect_vals()
        ]
    elif modifier == 'act_time':
        checks = [
            InputCheck(message.text).number_only(),
            InputCheck(message.text).check_time_value()
        ]
    else:
        checks = [
            InputCheck(message.text).check_comment_len(),
            InputCheck(message.text).check_incorrect_vals()
        ]
    # Check whether any of checks fail
    failed = []
    for x in checks:
        if type(x) is list:
            failed.append(x[1])
    if failed:
        failed = ' '.join(list(set(failed)))
        error_message = bot.send_message(
            message.from_user.id, 'Произошла ошибка. ' + failed)
        return bot.register_next_step_handler(error_message, process_action)
    # Fill in missing required columns
    if modifier == 'actl_name':
        cursor.execute(
            f'SELECT cat_name FROM "ACTIVITY" WHERE act_id = {act_id}')
        cat_name = cursor.fetchall()
        if cat_name:
            cat_name = cat_name[0][0]
        cursor.execute(f'INSERT INTO "ACTIVITY_LIST" (user_id, actl_name, cat_name) VALUES '
                       f'({user_id}, \'{message.text}\', \'{cat_name}\') ON CONFLICT DO NOTHING')
    elif modifier == 'cat_name':
        cursor.execute(f'INSERT INTO "CATEGORY" (cat_name, user_id) VALUES '
                       f'(\'{message.text}\', {user_id}) ON CONFLICT DO NOTHING')
        cursor.execute(
            f'SELECT actl_name FROM "ACTIVITY" WHERE act_id = {act_id}')
        actl_name = cursor.fetchall()
        if actl_name:
            actl_name = actl_name[0][0]
            cursor.execute(f'INSERT INTO "ACTIVITY_LIST" (user_id, actl_name, cat_name) VALUES '
                           f'({user_id}, \'{actl_name}\', \'{message.text}\') ON CONFLICT DO NOTHING')
    # Format entered date
    if modifier == 'act_date':
        value = datetime.strptime(
            message.text, '%d.%m.%Y').strftime('%Y-%m-%d')
    else:
        value = message.text
    # Update database with new info
    cursor.execute(
        f'UPDATE "ACTIVITY" SET {modifier} = \'{value}\' WHERE act_id = {act_id}')
    connection.commit()
    return edit_event(message)


@ bot.callback_query_handler(func=lambda callback: callback.data in ['date_sort', 'cat_sort'])
def callback_listener(callback):
    # Handle sorting button click
    if callback.data == 'cat_sort':
        display_events(callback, edit=True)
        bot.answer_callback_query(callback.id)
    else:
        display_events(callback, 'cat_sort', True)
        bot.answer_callback_query(callback.id)


def add_event(message):
    # Solve functions overlapping
    if message.text == '/start':
        return start_command(message)
    elif message.text == '/login':
        return login_command(message)
    elif message.text == '/display':
        return display_command(message)
    elif message.text.startswith('/open_') and len(message.text) > 6:
        return edit_event(message)
    elif message.text == '/add':
        return add_command(message)
    args = message.text.split(', ')
    if len(args) in range(4, 6):
        # Separate data to vars
        actl_name = args[0]
        act_time = args[1]
        act_date = datetime.now().strftime(
            '%Y-%m-%d') if args[2] == '-' else args[2]
        cat_name = args[3]
        act_comment = args[4] if len(args) == 5 else '(NULL)'
        # Check every entered field
        checks = [
            InputCheck(actl_name).check_len(),
            InputCheck(actl_name).check_incorrect_vals(),
            InputCheck(act_time).number_only(),
            InputCheck(act_time).check_time_value(),
            InputCheck(act_time).check_incorrect_vals(),
            InputCheck(act_date).check_date() if args[2] != '-' else True,
            InputCheck(act_date).check_incorrect_vals(),
            InputCheck(cat_name).check_len(),
            InputCheck(cat_name).check_incorrect_vals(),
            InputCheck(act_comment).check_comment_len() if len(
                args) == 5 else True,
            InputCheck(act_comment).check_incorrect_vals() if len(
                args) == 5 else True
        ]
        # Get error messages
        failed = []
        for x in checks:
            if type(x) is list:
                failed.append(x[1])
        if not failed:
            # Get user_id saved to the global dict
            try:
                user_id = users_data['user_id_' + str(message.from_user.id)]
            except KeyError:
                return bot.send_message(message.chat.id, 'Произошла ошибка.')
            # Insert the event into the database
            cursor.execute(f'INSERT INTO "CATEGORY" (user_id, cat_name) VALUES ({user_id}, \'{cat_name}\') '
                           f'ON CONFLICT DO NOTHING')
            cursor.execute(f'INSERT INTO "ACTIVITY_LIST" (user_id, actl_name, cat_name) VALUES '
                           f'({user_id}, \'{actl_name}\', \'{cat_name}\') ON CONFLICT DO NOTHING')
            cursor.execute(f'INSERT INTO "ACTIVITY" (user_id, actl_name, act_time, act_date, cat_name, act_comment) '
                           f'VALUES ({user_id}, \'{actl_name}\', \'{act_time}\', \'{act_date}\'::date, \'{cat_name}\', '
                           f'\'{act_comment}\') ON CONFLICT DO NOTHING')
            connection.commit()
            return bot.send_message(
                message.chat.id, 'Событие было успешно добавлено.')
        else:
            failed = ' '.join(list(set(failed)))
            error_message = bot.send_message(
                message.chat.id, 'Произошла ошибка.' + failed)
    elif len(args) > 5:
        error_message = bot.send_message(
            message.chat.id, 'Произошла ошибка. Слишком много запятых.')
    else:
        error_message = bot.send_message(
            message.chat.id, 'Произошла ошибка. Недостаточно полей было заполнено.')
    return bot.register_next_step_handler(error_message, add_event)


def remove_act_id(message):
    # Remove act_id from the global dict since the session is ended
    try:
        users_data.pop('act_id_' + str(message.from_user.id))
    except KeyError:
        pass


if __name__ == '__main__':
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            print(e)
