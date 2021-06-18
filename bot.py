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
    BOT_TOKEN = config.get('Bot', 'bot_token_sasha')
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


@bot.message_handler(func=lambda message: message.chat.type == 'private', commands=['start'])
def start_command(message):
    process_data(f'act_id_{message.from_user.id}', method='write', remove=True)
    bot.send_message(message.chat.id, 'Привет, для использования функционала бота войдите в '
                                      'аккаунт с помощью комманды /login')


@bot.message_handler(func=lambda message: message.chat.type == 'private', commands=['login'])
def login_command(message):
    process_data(f'act_id_{message.from_user.id}', method='write', remove=True)
    login_message = bot.send_message(message.chat.id, "Введите своё имя.")
    return bot.register_next_step_handler(login_message, check_login)


@bot.message_handler(func=lambda message: message.chat.type == 'private', commands=['display'])
def display_command(message):
    chat_id = message.chat.id
    process_data(f'act_id_{message.from_user.id}', method='write', remove=True)
    # Check whether the user is logged in
    if process_data(f'logged_in_{message.from_user.id}'):
        # Get current date in a certain format
        date = datetime.now().strftime('%d\\.%m\\.%Y')
        display_message = bot.send_message(chat_id, f'Какие даты отобразить?\n\n'
                                                    f'*Пример:*\n'
                                                    f'*\\-* — все события за сегодня '
                                                    f'\\(*{date}*\\)\\.\n'
                                                    f'*7* — за последние 7 дней\\.\n'
                                                    f'*01\\.06\\.2021* — конкретную дату\\.\n'
                                                    f'*01\\.01\\.2020, 01\\.01\\.2021* — '
                                                    f'все события между датами\\.',
                                           parse_mode='MarkdownV2')
        return bot.register_next_step_handler(display_message, display_events)
    else:
        bot.send_message(chat_id, 'Войдите в аккаунт с помощью комманды /login для использования '
                                  'этой функции.')


@bot.message_handler(func=lambda message: message.chat.type == 'private', commands=['add'])
def add_command(message):
    chat_id = message.chat.id
    process_data(f'act_id_{message.from_user.id}', method='write', remove=True)
    # Check whether the user is logged in
    if process_data(f'logged_in_{message.from_user.id}'):
        # Get current date in a certain format
        date = datetime.now().strftime('%d\\.%m\\.%Y')
        add_message = bot.send_message(chat_id, f'Добавьте новое событие\\.\n\n'
                                                f'*Необходимо ввести:*\n'
                                                f'Название события, затраченное время, дату '
                                                f'события, категорию, комментарий '
                                                f'\\(необязательно\\)\\.\n\n'
                                                f'Обратите внимание, для ввода даты можно '
                                                f'использовать следующие варианты ввода:\n'
                                                f'*\\-* — показать все события за сегодня '
                                                f'\\(*{date}*\\)\\.\n'
                                                f'*16\\.06\\.2021* — показать конкретную '
                                                f'дату\\.\n\n'
                                                f'*Например*:\n'
                                                f'Гулял, 42, 06\\.06\\.2021, Отдых, В парке\n'
                                                f'Смотрел фильм, 153, \\-, Отдых, Король лев\n'
                                                f'Готовил еду, 45, \\-, Быт\n',
                                       parse_mode='MarkdownV2')
        return bot.register_next_step_handler(add_message, add_event)
    else:
        bot.send_message(chat_id, 'Войдите в аккаунт с помощью комманды /login для использования '
                                  'этой функции.')


@bot.message_handler(func=lambda message: message.chat.type == 'private' and message.text.startswith('/open_'))
def edit_event(message):
    # Define common variables
    telegram_id = message.from_user.id
    txt = message.text
    chat_id = message.chat.id
    # Check whether the user is logged in
    if process_data(f'logged_in_{telegram_id}'):
        # If editing mode is being called by the command, set act_id to actual event's id
        if txt.startswith('/open_'):
            if len(txt) > 6:
                act_id = txt[6:]
            else:
                return bot.send_message(chat_id, 'Укажите идентификатор события.')
        else:
            try:
                act_id = process_data(f'act_id_{telegram_id}')
            except KeyError:
                act_id = txt[6:]
        # Check whether the event is available for the user
        try:
            user_id = process_data(f'user_id_{telegram_id}')
            cursor.execute(f'SELECT act_id FROM "ACTIVITY" where user_id = {user_id}')
            act_ids = cursor.fetchall()
            act_ids = [str(x[0]) for x in act_ids]
            if act_id not in act_ids:
                return bot.send_message(chat_id, 'Событие недоступно.')
        except (KeyError, DatabaseError):
            return bot.send_message(chat_id, 'Произошла ошибка.')
        # Save act_id to the global dict
        process_data(f'act_id_{telegram_id}', act_id, 'write')
        # Fetch event's data
        cursor.execute(f'SELECT act_date, actl_name, cat_name, act_time, act_comment '
                       f'FROM "ACTIVITY" WHERE act_id = {act_id}')
        data = cursor.fetchall()
        if data:
            act_date, actl_name, cat_name, act_time, act_comment = [str(x) for x in data[0]]
        else:
            return bot.send_message(chat_id, 'Произошла ошибка.')
        # Format data
        act_comment = act_comment if act_comment else '—'
        options = 'Дата: ' + act_date + ' /edit_date\n' + \
                  'Название: ' + actl_name + ' /edit_event\n' + \
                  'Категория: ' + cat_name + ' /edit_category\n' + \
                  'Время: ' + act_time + ' мин. /edit_time\n' + \
                  'Комментарий: ' + act_comment + ' /edit_comment\n' + \
                  'Удалить событие /delete_event\n' + \
                  'Выйти из режима просмотра /exit_event'
        bot.send_message(chat_id, f'Событие {act_id}!\n\n' + options)
    else:
        bot.send_message(chat_id, 'Войдите в аккаунт с помощью комманды /login для использования '
                                  'этой функции.')


@bot.message_handler(func=lambda message: message.chat.type == 'private' and message.text in specific_commands)
def choose_action(message):
    # Define common variables
    telegram_id = message.from_user.id
    txt = message.text
    chat_id = message.chat.id
    # Check whether the user is logged in
    if process_data(f'logged_in_{telegram_id}'):
        # Handle specific commands clicks
        if txt == '/edit_date':
            event_message = bot.send_message(chat_id, 'Введите дату.')
            process_data(f'modifier_{telegram_id}', 'act_date', 'write')
        elif txt == '/edit_event':
            event_message = bot.send_message(chat_id, 'Введите название.')
            process_data(f'modifier_{telegram_id}', 'actl_name', 'write')
        elif txt == '/edit_category':
            event_message = bot.send_message(chat_id, 'Введите категорию.')
            process_data(f'modifier_{telegram_id}', 'cat_name', 'write')
        elif txt == '/edit_time':
            event_message = bot.send_message(chat_id, 'Введите время.')
            process_data(f'modifier_{telegram_id}', 'act_time', 'write')
        elif txt == '/edit_comment':
            event_message = bot.send_message(chat_id, 'Введите комментарий.')
            process_data(f'modifier_{telegram_id}', 'act_comment', 'write')
        elif txt == '/delete_event':
            # Try and delete the event
            try:
                # Get act_id saved to the global dict
                try:
                    act_id = process_data(f'act_id_{telegram_id}')
                except KeyError:
                    return bot.send_message(chat_id, 'Произошла ошибка.')
                cursor.execute(f'DELETE FROM "ACTIVITY" WHERE act_id = {act_id}')
                connection.commit()
            except DatabaseError:
                bot.send_message(chat_id, 'Произошла ошибка.')
            process_data(f'act_id_{telegram_id}', method='write', remove=True)
            return display_events(message, refresh=True)
        else:
            process_data(f'act_id_{telegram_id}', method='write', remove=True)
            return display_events(message, refresh=True)
        return bot.register_next_step_handler(event_message, process_action)
    else:
        bot.send_message(chat_id, 'Войдите в аккаунт с помощью комманды /login для использования '
                                  'этой функции.')


def check_login(message):
    # Define common variables
    txt = message.text
    chat_id = message.chat.id
    # Solve functions overlapping
    if txt == '/start':
        return start_command(message)
    elif txt == '/login':
        return login_command(message)
    elif txt == '/display':
        return display_command(message)
    elif txt.startswith('/open_') and len(txt) > 6:
        return edit_event(message)
    elif txt == '/add':
        return add_command(message)
    check = [InputCheck(txt).check_incorrect_vals()]
    failed = [x[1] for x in check if type(x) is list]
    if failed:
        failed = ' '.join(list(set(failed)))
        error_message = bot.send_message(chat_id, 'Произошла ошибка. ' + failed)
        return bot.register_next_step_handler(error_message, check_login)
    # Fetch user_n_id with text entered by the user
    cursor.execute(f'SELECT user_n_id FROM "USER_NAME" WHERE user_n_name = \'{txt}\'')
    data = cursor.fetchall()
    if data:
        user_n_id = data[0][0]
        # Save user_n_id to the global dict
        process_data(f'user_n_id_{message.from_user.id}', user_n_id, 'write')
        password_message = bot.send_message(chat_id, 'Введите пароль.')
        return bot.register_next_step_handler(password_message, check_password)
    else:
        # User doesn't exist, tell the user to register
        error_message = bot.send_message(chat_id, 'Не удалось найти пользователя. Повторите '
                                                  'попытку или зарегистрируйся в приложении.')
        return bot.register_next_step_handler(error_message, check_login)


def check_password(message):
    # Define common variables
    telegram_id = message.from_user.id
    txt = message.text
    chat_id = message.chat.id
    # Solve functions overlapping
    if txt == '/start':
        return start_command(message)
    elif txt == '/login':
        return login_command(message)
    elif txt == '/display':
        return display_command(message)
    elif txt.startswith('/open_') and len(txt) > 6:
        return edit_event(message)
    elif txt == '/add':
        return add_command(message)
    # Get user_n_id saved to the global dict
    try:
        user_n_id = user_n_id = process_data(f'user_n_id_{telegram_id}')
    except KeyError:
        return bot.send_message(chat_id, 'Произошла ошибка.')
    check = [InputCheck(txt).check_incorrect_vals()]
    failed = [x[1] for x in check if type(x) is list]
    if failed:
        failed = ' '.join(list(set(failed)))
        error_message = bot.send_message(chat_id, 'Произошла ошибка. ' + failed)
        return bot.register_next_step_handler(error_message, check_password)
    # Fetch user_p_id with user_n_id we got from the check_login
    cursor.execute(f'SELECT user_p_id, user_id FROM "USER" WHERE user_n_id = \'{user_n_id}\'')
    data = cursor.fetchall()
    if data:
        user_p_id = data[0][0]
        user_id = data[0][1]
        # Save user_id to the global dict
        process_data(f'user_id_{telegram_id}', user_id, 'write')
        # Fetch user_p_password with user_p_id we got from the last step
        cursor.execute(f'SELECT user_p_password FROM "USER_PRIVATE" '
                       f'WHERE user_p_id = \'{user_p_id}\'')
        data = cursor.fetchall()
        if data:
            user_p_password = data[0][0]
            # Check entered password
            if txt == user_p_password:
                # Save logged state to the global dict
                process_data(f'logged_in_{telegram_id}', True, 'write')
                # Remove other ooccurencies of user_n_telegram
                cursor.execute(f'UPDATE "USER_NAME" SET user_n_telegram = NULL '
                               f'WHERE user_n_telegram = \'{telegram_id}\'')
                # Attach user_n_telegram to the current user's info
                cursor.execute(f'UPDATE "USER_NAME" SET user_n_telegram = \'{telegram_id}\''
                               f'WHERE user_n_id = \'{user_n_id}\'')
                connection.commit()
                bot.send_message(chat_id, 'Успешно.\n'
                                          'Для отображения событий используйте комманду /display\n'
                                          'Для добавления нового события используйте комманду '
                                          '/add')
            else:
                error_message = bot.send_message(chat_id, 'Неверный пароль. Повторите попытку.')
                # Reenter the same function if password is incorrect
                return bot.register_next_step_handler(error_message, check_password)
        else:
            # If couldn't get user_p_password
            bot.send_message(chat_id, 'Произошла ошибка.')
    else:
        # If couldn't get user_p_id
        bot.send_message(chat_id, 'Произошла ошибка.')


def display_events(message, sort_callback='date_sort', edit=False, refresh=False):
    if edit:
        # Accessing message attributes of CallbackQuery
        telegram_id = message.from_user.id
        message = message.message
    else:
        telegram_id = message.from_user.id
    chat_id = message.chat.id
    txt = message.text
    message_id = message.message_id
    if process_data(f'logged_in_{telegram_id}'):
        # Solve functions overlapping
        if not (edit or refresh):
            if txt == '/start':
                return start_command(message)
            elif txt == '/login':
                return login_command(message)
            elif txt == '/display':
                return display_command(message)
            elif txt.startswith('/open_') and len(txt) > 6:
                return edit_event(message)
            elif txt == '/add':
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
            user_id = process_data(f'user_id_{telegram_id}')
        except KeyError:
            return bot.send_message(chat_id, 'Произошла ошибка.')
        # Handle sorting button click
        if edit or refresh:
            try:
                txt = process_data(f'user_entry_{telegram_id}')
            except KeyError:
                if edit:
                    return bot.send_message(chat_id, 'Произошла ошибка.')
                else:
                    return bot.answer_callback_query(message.id)
        check = [InputCheck(txt).check_date() if txt != '-' else True,
                 InputCheck(txt).check_incorrect_vals()]
        failed = [x[1] for x in check if type(x) is list]
        if failed:
            failed = ' '.join(list(set(failed)))
            error_message = bot.send_message(chat_id, 'Произошла ошибка. ' + failed)
            return bot.register_next_step_handler(error_message, display_events)
        elif txt.isdigit():
            process_data(f'user_entry_{telegram_id}', txt, 'write')
            cursor.execute(f'SELECT * FROM "ACTIVITY" WHERE user_id = \'{user_id}\''
                           f'AND act_date >= (NOW()::date - \'{txt} days\'::interval) '
                           f'ORDER BY {sort_column} LIMIT 50')
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
            process_data(f'user_entry_{telegram_id}', txt, 'write')
            cursor.execute(f'SELECT * FROM "ACTIVITY" WHERE user_id = \'{user_id}\''
                           f'AND act_date = \'{date}\'::date '
                           f'ORDER BY {sort_column} LIMIT 50')
            activities_type = f'за {txt}'
        elif len(txt.split(', ')) == 2:
            process_data(f'user_entry_{telegram_id}', txt, 'write')
            date_1, date_2 = txt.split(', ')
            date_1_formatted, date_2_formatted = \
                [datetime.strptime(x, '%d.%m.%Y') for x in [date_1, date_2]]
            date_1_sorted, date_2_sorted = sorted([date_1_formatted, date_2_formatted])
            date_1_cleared, date_2_cleared = \
                [x.strftime('%Y-%m-%d') for x in [date_1_sorted, date_2_sorted]]
            sort_column += ' ASC' if date_1_formatted == date_1_sorted else ' DESC'
            cursor.execute(f'SELECT * FROM "ACTIVITY" WHERE user_id = \'{user_id}\''
                           f'AND act_date BETWEEN \'{date_1_cleared}\'::date '
                           f'AND \'{date_2_cleared}\'::date ORDER BY {sort_column} LIMIT 50')
            activities_type = 'с {0} по {1}'.format(date_1, date_2)
        else:
            error_message = bot.send_message(chat_id, 'Произошла ошибка. Неверный формат.')
            return bot.register_next_step_handler(error_message, display_events)
        data = cursor.fetchall()
        if data:
            # Make data readable
            activities_list = []
            for y in data:
                pointer = '> '
                date = y[4].strftime('%d.%m.%Y')
                name = str(y[2])
                category = f'({str(y[5])})'
                time = f'{str(y[3])}' + ' мин.'
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
            # Edit message with resorted events and replace the button to the opposite one
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                          reply_markup=markup)
            return
        else:
            bot.send_message(chat_id, text, reply_markup=markup)
    else:
        bot.send_message(chat_id, 'Войдите в аккаунт с помощью комманды /login для использования '
                                  'этой функции.')


def process_action(message):
    # Define common variables
    telegram_id = message.from_user.id
    txt = message.text
    chat_id = message.chat.id
    # Solve functions overlapping
    if txt == '/start':
        return start_command(message)
    elif txt == '/login':
        return login_command(message)
    elif txt == '/display':
        return display_command(message)
    elif txt.startswith('/open_') and len(txt) > 6:
        return edit_event(message)
    elif txt == '/add':
        return add_command(message)
    # Get user_id, modifier, act_id saved to the global dict
    try:
        user_id = process_data(f'user_id_{telegram_id}')
        modifier = process_data(f'modifier_{telegram_id}')
        act_id = process_data(f'act_id_{telegram_id}')
    except KeyError:
        return bot.send_message(chat_id, 'Произошла ошибка.')
    # Handle check for different modifiers
    if modifier == 'act_date':
        check = [InputCheck(txt).check_date(),
                 InputCheck(txt).check_incorrect_vals()]
    elif modifier == 'actl_name':
        check = [InputCheck(txt).check_len(),
                 InputCheck(txt).check_incorrect_vals()]
    elif modifier == 'cat_name':
        check = [InputCheck(txt).check_len(),
                 InputCheck(txt).check_incorrect_vals()]
    elif modifier == 'act_time':
        check = [InputCheck(txt).number_only(),
                 InputCheck(txt).check_time_value(),
                 InputCheck(txt).check_incorrect_vals()]
    else:
        check = [InputCheck(txt).check_comment_len(),
                 InputCheck(txt).check_incorrect_vals()]
    failed = [x[1] for x in check if type(x) is list]
    if failed:
        failed = ' '.join(list(set(failed)))
        error_message = bot.send_message(telegram_id, 'Произошла ошибка. ' + failed)
        return bot.register_next_step_handler(error_message, process_action)
    # Fill in missing required columns
    if modifier == 'actl_name':
        cursor.execute(f'SELECT cat_name FROM "ACTIVITY" WHERE act_id = {act_id}')
        cat_name = cursor.fetchall()
        if cat_name:
            cat_name = cat_name[0][0]
        cursor.execute(f'INSERT INTO "ACTIVITY_LIST" (user_id, actl_name, cat_name)'
                       f'VALUES ({user_id}, \'{txt}\', \'{cat_name}\') ON CONFLICT DO NOTHING')
    elif modifier == 'cat_name':
        cursor.execute(f'INSERT INTO "CATEGORY" (cat_name, user_id)'
                       f'VALUES (\'{txt}\', {user_id}) ON CONFLICT DO NOTHING')
        cursor.execute(f'SELECT actl_name FROM "ACTIVITY" WHERE act_id = {act_id}')
        actl_name = cursor.fetchall()
        if actl_name:
            actl_name = actl_name[0][0]
            cursor.execute(f'INSERT INTO "ACTIVITY_LIST" (user_id, actl_name, cat_name)'
                           f'VALUES ({user_id}, \'{actl_name}\', \'{txt}\')'
                           f'ON CONFLICT DO NOTHING')
    # Format entered date
    if modifier == 'act_date':
        value = datetime.strptime(txt, '%d.%m.%Y').strftime('%Y-%m-%d')
    else:
        value = txt
    # Update database with new info
    cursor.execute(f'UPDATE "ACTIVITY" SET {modifier} = \'{value}\' WHERE act_id = {act_id}')
    connection.commit()
    return edit_event(message)


@ bot.callback_query_handler(func=lambda callback: callback.data in ['date_sort', 'cat_sort'])
def callback_listener(callback):
    callback_id = callback.id
    # Handle sorting button click
    if callback.data == 'cat_sort':
        display_events(callback, edit=True)
        bot.answer_callback_query(callback_id)
    else:
        display_events(callback, 'cat_sort', True)
        bot.answer_callback_query(callback_id)


def add_event(message):
    # Define common variables
    txt = message.text
    chat_id = message.chat.id
    # Solve functions overlapping
    if txt == '/start':
        return start_command(message)
    elif txt == '/login':
        return login_command(message)
    elif txt == '/display':
        return display_command(message)
    elif txt.startswith('/open_') and len(txt) > 6:
        return edit_event(message)
    elif txt == '/add':
        return add_command(message)
    args = txt.split(', ')
    if len(args) in range(4, 6):
        # Separate data to vars
        actl_name = args[0]
        act_time = args[1]
        act_date = datetime.now().strftime('%Y-%m-%d') if args[2] == '-' else args[2]
        cat_name = args[3]
        act_comment = args[4] if len(args) == 5 else '(NULL)'
        # Check every entered field
        check = [InputCheck(actl_name).check_len(),
                 InputCheck(actl_name).check_incorrect_vals(),
                 InputCheck(act_time).number_only(),
                 InputCheck(act_time).check_time_value(),
                 InputCheck(act_time).check_incorrect_vals(),
                 InputCheck(act_date).check_date() if args[2] != '-' else True,
                 InputCheck(act_date).check_incorrect_vals(),
                 InputCheck(cat_name).check_len(),
                 InputCheck(cat_name).check_incorrect_vals(),
                 InputCheck(act_comment).check_comment_len() if len(args) == 5 else True,
                 InputCheck(act_comment).check_incorrect_vals() if len(args) == 5 else True]
        failed = [x[1] for x in check if type(x) is list]
        if not failed:
            # Get user_id saved to the global dict
            try:
                user_id = process_data(f'user_id_{message.from_user.id}')
            except KeyError:
                return bot.send_message(message.chat.id, 'Произошла ошибка.')
            # Insert the event into the database
            cursor.execute(f'INSERT INTO "CATEGORY" (user_id, cat_name)'
                           f'VALUES ({user_id}, \'{cat_name}\') '
                           f'ON CONFLICT DO NOTHING')
            cursor.execute(f'INSERT INTO "ACTIVITY_LIST" (user_id, actl_name, cat_name)'
                           f'VALUES ({user_id}, \'{actl_name}\', \'{cat_name}\')'
                           f'ON CONFLICT DO NOTHING')
            cursor.execute(f'INSERT INTO "ACTIVITY" (user_id, actl_name, act_time, act_date, '
                           f'cat_name, act_comment) VALUES ({user_id}, \'{actl_name}\', '
                           f'\'{act_time}\', \'{act_date}\'::date, \'{cat_name}\', '
                           f'\'{act_comment}\') ON CONFLICT DO NOTHING')
            connection.commit()
            return bot.send_message(chat_id, 'Событие было успешно добавлено.')
        else:
            failed = ' '.join(list(set(failed)))
            error_message = bot.send_message(chat_id, 'Произошла ошибка.' + failed)
    elif len(args) > 5:
        error_message = bot.send_message(chat_id, 'Произошла ошибка. Слишком много запятых.')
    else:
        error_message = bot.send_message(chat_id, 'Произошла ошибка. Недостаточно полей '
                                                  'было заполнено.')
    return bot.register_next_step_handler(error_message, add_event)


def process_data(key, value=None, method='read', remove=False):
    if key:
        out = {}
        # Read and format data from users_data.txt
        with open('users_data.txt', 'rb') as file:
            data = file.read()
            if len(data) != 0:
                data = data.split('\n')
                for line in data:
                    k, v = line.split('=')
                    out[k] = v
        # Write data into users_data.txt
        if method == 'write' and value:
            # Handle removing data
            if remove:
                try:
                    out.pop(key)
                except KeyError:
                    pass
            else:
                out[key] = value
            with open('users_data.txt', 'wb') as file:
                into_list, into = [], ''
                for k, v in out.items():
                    into_list.append(f'{k}={v}')
                into = '\n'.join(into_list)
                file.write(into)
            return True
        else:
            try:
                value = out[key]
            except KeyError:
                value = None
            return value
    return None


if __name__ == '__main__':
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            print(e)
