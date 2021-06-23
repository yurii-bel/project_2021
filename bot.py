import os
import telebot
import psycopg2
import configparser
import pickle

from psycopg2 import DatabaseError
from datetime import datetime
from telebot import types

from timeSoft import InputCheck


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

general_commands = ['/start',
                    '/login',
                    '/logout',
                    '/display',
                    '/add']
special_commands = ['/edit_title',
                    '/edit_time',
                    '/edit_date',
                    '/edit_category',
                    '/edit_comment',
                    '/delete_event',
                    '/exit_event']
options_titles = ['Название',
                  'Время',
                  'Дата',
                  'Категория',
                  'Комментарий']


def process_data(method='read', key=None, value=None, remove=None):
    # Implement pickle persistence
    if key or remove:
        file = 'users_data.pkl'
        # Create users_data.pkl if it does not exist
        if not os.path.isfile(file):
            open(file, 'a').close()
        # Read and format data
        with open(file, 'rb') as f:
            try:
                data = pickle.load(f)
            except EOFError:
                data = {}
        f.close()
        # Write data into users_data.pkl
        if method == 'write' and value:
            # Handle removing data
            if type(remove) == list:
                try:
                    for x in remove:
                        data.pop(x)
                except KeyError:
                    pass
            # Handle adding data
            else:
                data[key] = value
            with open(file, 'wb') as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
            f.close()
            return True
        else:
            try:
                value = data[key]
            except KeyError:
                value = None
            return value
    return None


@bot.message_handler(func=lambda m: m.chat.type == 'private', commands=['start'])
def start_command(m):
    process_data(method='write', remove=[f'act_id_{m.from_user.id}'])
    bot.send_message(m.chat.id, 'Привет, для использования функционала бота войдите в аккаунт с '
                                'помощью комманды /login')


@bot.message_handler(func=lambda m: m.chat.type == 'private', commands=['login'])
def login_command(m):
    process_data(method='write', remove=[f'act_id_{m.from_user.id}'])
    login_message = bot.send_message(m.chat.id, "Введите своё имя.")
    return bot.register_next_step_handler(login_message, check_login)


@bot.message_handler(func=lambda m: m.chat.type == 'private', commands=['logout'])
def logout_command(m):
    telegram_id = m.from_user.id
    chat_id = m.chat.id
    # Fetch user_n_telegram
    try:
        cursor.execute(f'SELECT user_n_telegram FROM "USER_NAME" '
                       f'WHERE user_n_telegram = \'{telegram_id}\'')
        data = cursor.fetchall()
    except DatabaseError:
        return error_handler(m)
    if data:
        # Remove user's occurrence of user_n_telegram
        try:
            cursor.execute(f'UPDATE "USER_NAME" SET user_n_telegram = (NULL) '
                           f'WHERE user_n_telegram = \'{telegram_id}\'')
        except DatabaseError:
            return error_handler(m)
        # Remove act_id, logged_in, user_n_id, user_id, user_entry and modifier
        process_data(method='write', remove=[f'act_id_{telegram_id}',
                                             f'logged_in_{telegram_id}'
                                             f'user_n_id_{telegram_id}',
                                             f'user_id_{telegram_id}'
                                             f'user_entry_{telegram_id}',
                                             f'modifier_{telegram_id}'])
        bot.send_message(chat_id, 'Вы успешно вышли из аккаунта.')
    else:
        bot.send_message(chat_id, 'Вы не вошли в аккаунт.')


@bot.message_handler(func=lambda m: m.chat.type == 'private', commands=['display'])
def display_command(m):
    telegram_id = m.from_user.id
    chat_id = m.chat.id
    process_data(method='write', remove=[f'act_id_{telegram_id}'])
    # Check whether the user is logged in
    if process_data(key=f'logged_in_{telegram_id}'):
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


@bot.message_handler(func=lambda m: m.chat.type == 'private', commands=['add'])
def add_command(m):
    telegram_id = m.from_user.id
    chat_id = m.chat.id
    process_data(method='write', remove=[f'act_id_{telegram_id}'])
    # Check whether the user is logged in
    if process_data(key=f'logged_in_{telegram_id}'):
        # Get current date in a certain format
        date = datetime.now().strftime('%d\\.%m\\.%Y')
        add_message = bot.send_message(chat_id, f'Добавьте новое событие\\.\n\n'
                                                f'*Необходимо ввести:*\n'
                                                f'Название события, затраченное время, дату '
                                                f'события, категорию и комментарий '
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


def check_login(m):
    # Define common variables
    txt = m.text
    chat_id = m.chat.id
    telegram_id = m.from_user.id
    # Solve functions overlapping
    if txt == general_commands[0]:
        return start_command(m)
    elif txt == general_commands[1]:
        return login_command(m)
    elif txt == general_commands[2]:
        return logout_command(m)
    elif txt == general_commands[3]:
        return display_command(m)
    elif txt.startswith('/open') and len(txt) > 6 and txt[6:].isdigit():
        return edit_event(m)
    elif txt == general_commands[4]:
        return add_command(m)
    elif txt in special_commands:
        return choose_action(m)
    check = [InputCheck(txt).check_incorrect_vals()]
    failed = [x[1] for x in check if type(x) is list]
    if failed:
        failed = ' '.join(list(set(failed)))
        error_message = bot.send_message(chat_id, f'{failed}\nПовторите попытку.')
        return bot.register_next_step_handler(error_message, check_login)
    # Fetch user_n_telegram with the text entered by the user
    try:
        cursor.execute(f'SELECT user_n_telegram FROM "USER_NAME" WHERE user_n_name = \'{txt}\'')
        data = cursor.fetchall()
    except DatabaseError:
        return error_handler(m)
    if data:
        if not data[0][0] or data[0][0] == str(telegram_id):
            # Remove user's occurrence of user_n_telegram
            try:
                cursor.execute(f'UPDATE "USER_NAME" SET user_n_telegram = (NULL) '
                               f'WHERE user_n_telegram = \'{telegram_id}\'')
            except DatabaseError:
                return error_handler(m)
            # Remove act_id, logged_in, user_n_id, user_id, user_entry and modifier
            process_data(method='write', remove=[f'act_id_{telegram_id}',
                                                 f'logged_in_{telegram_id}'
                                                 f'user_n_id_{telegram_id}',
                                                 f'user_id_{telegram_id}'
                                                 f'user_entry_{telegram_id}',
                                                 f'modifier_{telegram_id}'])
        else:
            # User has already been logged in, tell the user to log out
            error_message = bot.send_message(chat_id, 'Пользователь уже был авторизован под '
                                                      'другим телеграм аккаунтом\\. Если этот '
                                                      'телеграм аккаунт принадлежит вам, '
                                                      'выйдите из него помощью комманды '
                                                      '`/logout`\\.',
                                             parse_mode='MarkdownV2')
            return bot.register_next_step_handler(error_message, check_login)
    # Fetch user_n_id with text entered by the user
    try:
        cursor.execute(f'SELECT user_n_id FROM "USER_NAME" WHERE user_n_name = \'{txt}\'')
        data = cursor.fetchall()
    except DatabaseError:
        return error_handler(m)
    if data:
        user_n_id = data[0][0]
        # Save user_n_id
        process_data('write', f'user_n_id_{m.from_user.id}', user_n_id)
        password_message = bot.send_message(chat_id, 'Введите пароль.')
        return bot.register_next_step_handler(password_message, check_password)
    else:
        # User does not exist, tell the user to register
        error_message = bot.send_message(chat_id, 'Не удалось найти пользователя. '
                                                  'Повторите попытку или '
                                                  'зарегистрируйтесь в приложении.')
        return bot.register_next_step_handler(error_message, check_login)


def check_password(m):
    # Define common variables
    telegram_id = m.from_user.id
    txt = m.text
    chat_id = m.chat.id
    # Solve functions overlapping
    if txt == general_commands[0]:
        return start_command(m)
    elif txt == general_commands[1]:
        return login_command(m)
    elif txt == general_commands[2]:
        return logout_command(m)
    elif txt == general_commands[3]:
        return display_command(m)
    elif txt.startswith('/open') and len(txt) > 6 and txt[6:].isdigit():
        return edit_event(m)
    elif txt == general_commands[4]:
        return add_command(m)
    elif txt in special_commands:
        return choose_action(m)
    # Get user_n_id
    user_n_id = process_data(key=f'user_n_id_{telegram_id}')
    if not user_n_id:
        return error_handler(m)
    check = [InputCheck(txt).check_incorrect_vals()]
    failed = [x[1] for x in check if type(x) is list]
    if failed:
        failed = ' '.join(list(set(failed)))
        error_message = bot.send_message(chat_id, f'{failed}\nПовторите попытку.')
        return bot.register_next_step_handler(error_message, check_password)
    # Fetch user_p_id with user_n_id we got from the check_login
    try:
        cursor.execute(f'SELECT user_p_id, user_id FROM "USER" WHERE user_n_id = \'{user_n_id}\'')
        data = cursor.fetchall()
    except DatabaseError:
        return error_handler(m)
    if data:
        user_p_id = data[0][0]
        user_id = data[0][1]
        # Save user_id
        process_data('write', f'user_id_{telegram_id}', user_id)
        # Fetch user_p_password with user_p_id we got from the last step
        try:
            cursor.execute(f'SELECT user_p_password FROM "USER_PRIVATE" '
                           f'WHERE user_p_id = \'{user_p_id}\'')
            data = cursor.fetchall()
        except DatabaseError:
            return error_handler(m)
        if data:
            user_p_password = data[0][0]
            # Check entered password
            if txt == user_p_password:
                # Save logged state
                process_data('write', f'logged_in_{telegram_id}', True)
                # Try and attach user_n_telegram to the current user's info
                try:
                    cursor.execute(f'UPDATE "USER_NAME" SET user_n_telegram = \'{telegram_id}\''
                                   f'WHERE user_n_id = \'{user_n_id}\'')
                except DatabaseError:
                    return error_handler(m)
                connection.commit()
                bot.send_message(chat_id, 'Успешно.\n'
                                          'Для отображения событий используйте комманду /display\n'
                                          'Для добавления нового события используйте комманду '
                                          '/add')
            else:
                error_message = bot.send_message(chat_id, 'Неверный пароль.\nПовторите попытку.')
                # Reenter the same function if password is incorrect
                return bot.register_next_step_handler(error_message, check_password)
        else:
            # If couldn't get user_p_password
            return error_handler(m)
    else:
        # If couldn't get user_p_id
        return error_handler(m)


def display_events(m, sort_callback='date_sort', edit=False, refresh=False):
    if edit:
        # Accessing message attributes of CallbackQuery
        telegram_id = m.from_user.id
        m = m.message
    else:
        telegram_id = m.from_user.id
    chat_id = m.chat.id
    txt = m.text
    if process_data(key=f'logged_in_{telegram_id}'):
        # Solve functions overlapping
        if not (edit or refresh):
            if txt == general_commands[0]:
                return start_command(m)
            elif txt == general_commands[1]:
                return login_command(m)
            elif txt == general_commands[2]:
                return logout_command(m)
            elif txt == general_commands[3]:
                return display_command(m)
            elif txt.startswith('/open') and len(txt) > 6 and txt[6:].isdigit():
                return edit_event(m)
            elif txt == general_commands[4]:
                return add_command(m)
            elif txt in special_commands:
                return choose_action(m)
        # Define sorting vars needed for activities sorting and sorting button name
        if sort_callback == 'cat_sort':
            sort_column = 'cat_name'
            sort_type = 'датам'
        else:
            sort_column = 'act_date'
            sort_type = 'категориям'
        # Get user_id
        user_id = process_data(key=f'user_id_{telegram_id}')
        if not user_id:
            return error_handler(m)
        # Handle sorting button click
        if edit or refresh:
            txt = process_data(key=f'user_entry_{telegram_id}')
            if not txt:
                if edit:
                    return bot.answer_callback_query(m.id)
                else:
                    return error_handler(m)
        check = [InputCheck(txt).check_date() if txt != '-' else True,
                 InputCheck(txt).check_incorrect_vals()]
        failed = [x[1] for x in check if type(x) is list]
        if failed:
            failed = ' '.join(list(set(failed)))
            error_message = bot.send_message(chat_id, f'{failed}\nПовторите попытку.')
            return bot.register_next_step_handler(error_message, display_events)
        elif txt.isdigit():
            process_data('write', f'user_entry_{telegram_id}', txt)
            query = f'SELECT * FROM "ACTIVITY" WHERE user_id = \'{user_id}\'' \
                    f'AND act_date >= (NOW()::date - \'{txt} days\'::interval) ' \
                    f'ORDER BY {sort_column} LIMIT 50'
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
            process_data('write', f'user_entry_{telegram_id}', txt)
            query = f'SELECT * FROM "ACTIVITY" WHERE user_id = \'{user_id}\'' \
                    f'AND act_date = \'{date}\'::date ' \
                    f'ORDER BY {sort_column} LIMIT 50'
            activities_type = f'за {txt}'
        elif len(txt.split(', ')) == 2:
            process_data('write', f'user_entry_{telegram_id}', txt)
            date_1, date_2 = txt.split(', ')
            date_1_formatted, date_2_formatted = \
                [datetime.strptime(x, '%d.%m.%Y') for x in [date_1, date_2]]
            date_1_sorted, date_2_sorted = sorted([date_1_formatted, date_2_formatted])
            date_1_cleared, date_2_cleared = \
                [x.strftime('%Y-%m-%d') for x in [date_1_sorted, date_2_sorted]]
            sort_column += ' ASC' if date_1_formatted == date_1_sorted else ' DESC'
            query = f'SELECT * FROM "ACTIVITY" WHERE user_id = \'{user_id}\'' \
                    f'AND act_date BETWEEN \'{date_1_cleared}\'::date ' \
                    f'AND \'{date_2_cleared}\'::date ORDER BY {sort_column} LIMIT 50'
            activities_type = 'с {0} по {1}'.format(date_1, date_2)
        else:
            error_message = bot.send_message(chat_id, 'Неверный формат.\nПовторите попытку.')
            return bot.register_next_step_handler(error_message, display_events)
        try:
            cursor.execute(query)
            data = cursor.fetchall()
        except DatabaseError:
            return error_handler(m)
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
                button = types.InlineKeyboardButton(f'Сортировать по {sort_type}',
                                                    callback_data=sort_callback)
                markup = keyboard.add(button)
            else:
                markup = None
        else:
            text = 'Активности отсутствуют.'
            markup = None
        # Handle sorting button click
        if edit:
            message_id = m.message_id
            # Edit the message with resorted events and replace the button to the opposite one
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                          reply_markup=markup)
            return
        else:
            if refresh:
                process_data(method='write', remove=[f'act_id_{telegram_id}'])
            bot.send_message(chat_id, text, reply_markup=markup)
    else:
        bot.send_message(chat_id, 'Войдите в аккаунт с помощью комманды /login для использования '
                                  'этой функции.')


@bot.message_handler(func=lambda m: m.chat.type == 'private' and m.text.startswith('/open'))
def edit_event(m):
    # Define common variables
    telegram_id = m.from_user.id
    txt = m.text
    chat_id = m.chat.id
    # Check whether the user is logged in
    if process_data(key=f'logged_in_{telegram_id}'):
        # If editing mode is being called by the command, set act_id to actual event's id
        if txt.startswith('/open_'):
            if len(txt) > 6:
                act_id = txt[6:]
            else:
                return bot.send_message(chat_id, 'Укажите идентификатор события.')
        else:
            act_id = process_data(key=f'act_id_{telegram_id}')
            if not act_id:
                act_id = txt[6:]
        # Check whether the event is available for the user
        user_id = process_data(key=f'user_id_{telegram_id}')
        if not user_id:
            return error_handler(m)
        try:
            cursor.execute(f'SELECT act_id FROM "ACTIVITY" where user_id = {user_id}')
            act_ids = cursor.fetchall()
        except DatabaseError:
            return error_handler(m)
        act_ids = [str(x[0]) for x in act_ids]
        if act_id not in act_ids:
            return bot.send_message(chat_id, 'Событие недоступно.')
        # Save act_id
        process_data('write', f'act_id_{telegram_id}', act_id)
        # Fetch event's data
        try:
            cursor.execute(f'SELECT actl_name, act_time, act_date, cat_name, act_comment '
                           f'FROM "ACTIVITY" WHERE act_id = {act_id}')
            data = cursor.fetchall()
        except DatabaseError:
            return error_handler(m)
        if data:
            # Format data
            actl_name, act_time, act_date, cat_name, act_comment = data[0]
            act_date = datetime.combine(act_date, datetime.min.time()).strftime('%d.%m.%Y')
            act_comment = act_comment if act_comment else '—'
            options = f'{options_titles[0]}: {actl_name} {special_commands[0]}\n' + \
                      f'{options_titles[1]}: {act_time} {special_commands[1]}\n' + \
                      f'{options_titles[2]}: {act_date} {special_commands[2]}\n' + \
                      f'{options_titles[3]}: {cat_name} мин. {special_commands[3]}\n' + \
                      f'{options_titles[4]}: {act_comment} {special_commands[4]}\n' + \
                      f'Удалить событие {special_commands[5]}\n' + \
                      f'Выйти из режима просмотра {special_commands[6]}'
            bot.send_message(chat_id, f'Событие {act_id}!\n\n' + options)
        else:
            return error_handler(m)
    else:
        bot.send_message(chat_id, 'Войдите в аккаунт с помощью комманды /login для использования '
                                  'этой функции.')


@bot.message_handler(func=lambda m: m.chat.type == 'private' and m.text in special_commands)
def choose_action(m):
    # Define common variables
    telegram_id = m.from_user.id
    txt = m.text
    chat_id = m.chat.id
    # Check whether the user is logged in
    if process_data(key=f'logged_in_{telegram_id}'):
        # Handle specific commands clicks
        if txt == special_commands[0]:
            event_message = bot.send_message(chat_id, 'Введите название.')
            process_data('write', f'modifier_{telegram_id}', 'actl_name')
        elif txt == special_commands[1]:
            event_message = bot.send_message(chat_id, 'Введите время.')
            process_data('write', f'modifier_{telegram_id}', 'act_time')
        elif txt == special_commands[2]:
            event_message = bot.send_message(chat_id, 'Введите дату.')
            process_data('write', f'modifier_{telegram_id}', 'act_date')
        elif txt == special_commands[3]:
            event_message = bot.send_message(chat_id, 'Введите категорию.')
            process_data('write', f'modifier_{telegram_id}', 'cat_name')
        elif txt == special_commands[4]:
            event_message = bot.send_message(chat_id, 'Введите комментарий.')
            process_data('write', f'modifier_{telegram_id}', 'act_comment')
        elif txt == special_commands[5]:
            # Try and delete the event
            # Get act_id
            act_id = process_data(key=f'act_id_{telegram_id}')
            if not act_id:
                return error_handler(m)
            try:
                cursor.execute(f'DELETE FROM "ACTIVITY" WHERE act_id = {act_id}')
                connection.commit()
            except DatabaseError:
                return error_handler(m)
            return display_events(m, refresh=True)
        else:
            return display_events(m, refresh=True)
        return bot.register_next_step_handler(event_message, process_action)
    else:
        bot.send_message(chat_id, 'Войдите в аккаунт с помощью комманды /login для использования '
                                  'этой функции.')


def process_action(m):
    # Define common variables
    telegram_id = m.from_user.id
    txt = m.text
    # Solve functions overlapping
    if txt == general_commands[0]:
        return start_command(m)
    elif txt == general_commands[1]:
        return login_command(m)
    elif txt == general_commands[2]:
        return logout_command(m)
    elif txt == general_commands[3]:
        return display_command(m)
    elif txt.startswith('/open') and len(txt) > 6 and txt[6:].isdigit():
        return edit_event(m)
    elif txt == general_commands[4]:
        return add_command(m)
    elif txt in special_commands:
        return choose_action(m)
    # Get user_id, modifier and act_id
    user_id = process_data(key=f'user_id_{telegram_id}')
    modifier = process_data(key=f'modifier_{telegram_id}')
    act_id = process_data(key=f'act_id_{telegram_id}')
    if not user_id or not modifier or not act_id:
        return error_handler(m)
    # Handle check for different modifiers
    if modifier == 'actl_name':
        check = [InputCheck(txt).check_len(),
                 InputCheck(txt).check_incorrect_vals()]
    elif modifier == 'act_time':
        check = [InputCheck(txt).number_only(),
                 InputCheck(txt).check_time_value(),
                 InputCheck(txt).check_incorrect_vals()]
    elif modifier == 'act_date':
        check = [InputCheck(txt).check_date() if txt != '-' else True,
                 InputCheck(txt).check_incorrect_vals()]
    elif modifier == 'cat_name':
        check = [InputCheck(txt).check_len(),
                 InputCheck(txt).check_incorrect_vals()]
    elif modifier == 'act_comment':
        check = [InputCheck(txt).check_comment_len(),
                 InputCheck(txt).check_incorrect_vals()]
    else:
        return error_handler(m)
    failed = [x[1] for x in check if type(x) is list]
    if failed:
        failed = ' '.join(list(set(failed)))
        error_message = bot.send_message(telegram_id, f'{failed}\nПовторите попытку.')
        return bot.register_next_step_handler(error_message, process_action)
    # Fill in missing required columns
    if modifier == 'actl_name':
        try:
            cursor.execute(f'SELECT cat_name FROM "ACTIVITY" WHERE act_id = {act_id}')
            cat_name = cursor.fetchall()
        except DatabaseError:
            return error_handler(m)
        if cat_name:
            cat_name = cat_name[0][0]
            try:
                cursor.execute(f'INSERT INTO "ACTIVITY_LIST" (user_id, actl_name, cat_name)'
                               f'VALUES ({user_id}, \'{txt}\', \'{cat_name}\')'
                               f'ON CONFLICT DO NOTHING')
            except DatabaseError:
                return error_handler(m)
    elif modifier == 'cat_name':
        try:
            cursor.execute(f'INSERT INTO "CATEGORY" (cat_name, user_id)'
                           f'VALUES (\'{txt}\', {user_id}) ON CONFLICT DO NOTHING')
            cursor.execute(f'SELECT actl_name FROM "ACTIVITY" WHERE act_id = {act_id}')
            actl_name = cursor.fetchall()
        except DatabaseError:
            return error_handler(m)
        if actl_name:
            actl_name = actl_name[0][0]
            try:
                cursor.execute(f'INSERT INTO "ACTIVITY_LIST" (user_id, actl_name, cat_name)'
                               f'VALUES ({user_id}, \'{actl_name}\', \'{txt}\')'
                               f'ON CONFLICT DO NOTHING')
            except DatabaseError:
                return error_handler(m)
    # Format entered date
    if modifier == 'act_date':
        value = datetime.strptime(txt, '%d.%m.%Y').strftime('%Y-%m-%d')
    else:
        value = txt
    # Update database with new info
    try:
        cursor.execute(f'UPDATE "ACTIVITY" SET {modifier} = \'{value}\' WHERE act_id = {act_id}')
        connection.commit()
    except DatabaseError:
        return error_handler(m)
    return edit_event(m)


@bot.callback_query_handler(func=lambda callback: callback.data in ['date_sort', 'cat_sort'])
def callback_listener(callback):
    callback_id = callback.id
    # Handle sorting button click
    if callback.data == 'cat_sort':
        display_events(callback, edit=True)
        bot.answer_callback_query(callback_id)
    else:
        display_events(callback, 'cat_sort', True)
        bot.answer_callback_query(callback_id)


def add_event(m):
    # Define common variables
    chat_id = m.chat.id
    txt = m.text
    # Solve functions overlapping
    if txt == general_commands[0]:
        return start_command(m)
    elif txt == general_commands[1]:
        return login_command(m)
    elif txt == general_commands[2]:
        return logout_command(m)
    elif txt == general_commands[3]:
        return display_command(m)
    elif txt.startswith('/open') and len(txt) > 6 and txt[6:].isdigit():
        return edit_event(m)
    elif txt == general_commands[4]:
        return add_command(m)
    elif txt in special_commands:
        return choose_action(m)
    args = txt.split(', ')
    if len(args) in range(4, 6):
        # Handle rejecting command entered
        fields, entries = [], []
        for i, x in enumerate(args):
            for y in general_commands + special_commands:
                if y in x:
                    fields.append(f'`{options_titles[i]}`')
                    entries.append(f'`{x}`')
            if x.startswith('/open'):
                if x.startswith('/open_') and len(x) > 6 and x[6:].isdigit():
                    fields.append(f'`{options_titles[i]}`')
                    entries.append(f'`/open\\_{x[6:]}`')
                else:
                    fields.append(f'`{options_titles[i]}`')
                    entries.append('`/open`')
        if fields and entries:
            if len(fields) == 1:
                field = f'поле {fields[0]}'
            else:
                field = f"поля \\({', '.join(fields)}\\)"
            if len(entries) == 1:
                entry = f'была введена комманда {entries[0]}'
            else:
                entry = f"были введены комманды \\({', '.join(entries)}\\)"
            error_message = bot.send_message(chat_id, f'В {field} {entry}\\.'
                                                      f'\nПовторите попытку\\.',
                                             parse_mode='MarkdownV2')
            return bot.register_next_step_handler(error_message, add_event)
        # Separate data to vars
        actl_name = args[0]
        act_time = args[1]
        act_date = datetime.now().strftime('%Y-%m-%d') if args[2] == '-' else args[2]
        cat_name = args[3]
        act_comment = args[4] if len(args) == 5 else '(NULL)'
        # Check every entered field
        check = [InputCheck(act_date).check_date() if args[2] != '-' else True,
                 InputCheck(act_date).check_incorrect_vals(),
                 InputCheck(actl_name).check_len(),
                 InputCheck(actl_name).check_incorrect_vals(),
                 InputCheck(cat_name).check_len(),
                 InputCheck(cat_name).check_incorrect_vals(),
                 InputCheck(act_time).number_only(),
                 InputCheck(act_time).check_time_value(),
                 InputCheck(act_time).check_incorrect_vals(),
                 InputCheck(act_comment).check_comment_len() if len(args) == 5 else True,
                 InputCheck(act_comment).check_incorrect_vals() if len(args) == 5 else True]
        failed = [x[1] for x in check if type(x) is list]
        if not failed:
            # Get user_id
            user_id = process_data(key=f'user_id_{m.from_user.id}')
            if not user_id:
                return error_handler(m)
            # Insert the event into the database
            try:
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
            except DatabaseError:
                return error_handler(m)
            return bot.send_message(chat_id, 'Событие было успешно добавлено.')
        else:
            failed = ' '.join(list(set(failed)))
            error_message = bot.send_message(chat_id, f'{failed}.\nПовторите попытку.')
    elif len(args) > 5:
        error_message = bot.send_message(chat_id, 'Слишком много запятых.\n'
                                                  'Повторите попытку.')
    else:
        error_message = bot.send_message(chat_id, 'Недостаточно полей было заполнено.\n'
                                                  'Повторите попытку.')
    return bot.register_next_step_handler(error_message, add_event)


def error_handler(m):
    return bot.send_message(m.chat.id, 'Произошла ошибка.')


if __name__ == '__main__':
    bot.infinity_polling(timeout=10, long_polling_timeout=10)
