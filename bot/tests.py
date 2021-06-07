
from bot.get_activities import Expense
# import logging

# from aiogram import Bot, Dispatcher as dp, executor, types
# from aiogram.dispatcher.dispatcher import Dispatcher
# import psycopg2 as db
# import os
# import datetime
# import re
# from typing import List, NamedTuple, Optional

# import pytz



# """

#                                     Add activities!

# """



# class Message(NamedTuple):
#     """Структура распаршенного сообщения о новом расходе"""
#     amount: int
#     category_text: str


# class Activities(NamedTuple):
#     """Структура добавленного в БД нового расхода"""
#     id: Optional[int]
#     amount: int
#     category_name: str


# def add_activities(raw_message: str) -> Expense:
#     """Добавляет новое сообщение.
#     Принимает на вход текст сообщения, пришедшего в бот."""

#     parsed_message = _parse_message(raw_message)
#     category = Categories().get_category(
#         parsed_message.category_text)
#     inserted_row_id = db.insert("expense", {
#         "amount": parsed_message.amount,
#         "created": _get_now_formatted(),
#         "category_codename": category.codename,
#         "raw_text": raw_message
#     })
#     return Expense(id=None,
#                 amount=parsed_message.amount,
#                 category_name=category.name)


# def get_today_activities() -> str:
#     """ Is returned to str statisticks for today """
#     cursor = db.get_cursor()
#     cursor.execute("select sum(amount) "
#                 "from expense where date(created)=date('now', 'localtime')")#Переделать когда придет Дима
#     result = cursor.fetchone()
#     if not result[0]:
#         return "Today activities is not defined"
#     all_today_activities = result[0]
#     cursor.execute("select sum(amount) "
#                 "from expense where date(created)=date('now', 'localtime') "
#                 "and category_codename in (select codename "
#                 "from category where is_base_expense=true)")#Переделать когда придет Дима
#     result = cursor.fetchone()
#     base_today_expenses = result[0] if result[0] else 0
#     return (f"Activities for today :\n"
#             f" — {all_today_activities} for the day.\n"
#             f" for: /month")



# TOKEN = os.getenv('my_id_tg')

# db_name = 'dt1vdgsvah47r'
# db_user = 'ryxcgrjdgvrsxx'
# db_password = '2e4d8cbc5b0f94259507584c6868f20ae0d4da79fdc618f6c2602d18045b2b61'
# db_host = 'ec2-54-74-60-70.eu-west-1.compute.amazonaws.com'




# connection = db.connect(database = db_name, user = db_user, password = db_password, host = db_host)

# #create logg
# logging.basicConfig(level=logging.INFO)

    

# cursor = connection.cursor()
# bot = Bot(token = TOKEN)
# dp = Dispatcher(bot)


# '''

# Messagage handler triggerin oncommands start,
# and get help what we can to do 

# '''

# @dp.message_handler(commands=['start'])
# async def start_bot(message:types.Message):
#     await message.reply(
#             "Bot was get your activities of day\n\n"
#             "Add activieies: run \n"
#             "Today activities: /today\n"
#             "All the current munth: /month\n"
#             "Last gettin updates activities\n",
#             reply=False
#         )


# @dp.message_handler(commands=['today'])
# async def today_activities(Message:types.Message):
#     """ Отпрвляет сегодняшние активности """

# @dp.message_handler()
# async def add_activities(message:types.Message):
#     '''Добавляет новую активность'''
#     try:
#         activites = get_activities.add_activities #в оригинальном коде это не активности а expence
#     except exeption.NotCorrectMessage as e:
#         await message.answer(str(e))
#         return
#     answer_message = (
#         f"Add activities {get_activites.category_name}.\n\n"
#         f"Get today activities {get_activities.get_today_statistic}")
#     await message.answer(answer_message)


# """

#                                     Add activities!

# """



# if __name__ == '__main__': 
#     executor.start_polling(dp, skip_updates=True)
tk = '1891194594:AAGDaHHTuZv5mDBIV8Q4Sjd7xU1RPPry0ns'

import time
import psycopg2 as db 
import telebot


db_name = 'dt1vdgsvah47r'
db_user = 'ryxcgrjdgvrsxx'
db_password = '2e4d8cbc5b0f94259507584c6868f20ae0d4da79fdc618f6c2602d18045b2b61'
db_host = 'ec2-54-74-60-70.eu-west-1.compute.amazonaws.com'


connection = db.connect(database = db_name, user = db_user, password = db_password, host = db_host)

cursor = connection.cursor()
correct_login_info = False
bot = telebot.TeleBot(tk)

#АВТОРИЗАЦИЯ ПОЛЬЗОВАТЕЛЯ
#настроить команду старт чтобы при нажатии , я видел сообщение привет , пожалуйста залогинься команда (логин)
#чувак вводит (ком.логин) : 
# 1 введите ваше имя из приложения тайм-софт
# 2 введите ваш id из приложения тайм-софт
# если пользователь существует , то пользователь успешно зарегистрирован , если нет то скачайте по ссылке

@bot.message_handler(commands=['start'])
def welcome_func(message):
    bot.send_message(message.chat.id,"Hey!,  if u want to login please get the command '/login'")



@bot.message_handler(commands=['login'])
def message_about_name(message_l):
        bot.send_message(message_l.chat.id,"Please enter your name, id  from app\
            'Time_soft' across comand '/имя_пользователя', '/пароль_пользователя'")





# def input_category(message):
#     x = bot.send_message(message.chat.id,'Input category name')
#     bot.register_next_step_handler(x,get_category)


# def get_category(message_3):
#     user_category = message_3.text 
#     print(user_category)


#ПРОВЕРКА
#Если пользователь существует то вывести его имя , id 


# @bot.message_handler(commands = ['categories'])
# def add_action(message):
#     m_id_2 = message.chat.id
#     cursor.execute('INSERT INTO "CATEGORY" (user_id,cat_name) VALUES (%s,%s)'.format(sql.Identifier(m_id_2)))
#     f = connection.commit()
#     bot.send_message(message,'Data inserted sucsefully')
#     connection.close(m_id_2,f)

# @bot.message_handler(commands = ['input_data'])
# def input_data(message):
#     z = bot.send_message(message.chat.id,'Input user id: ')
#     bot.register_next_step_handler(z,get_id)
    



@bot.message_handler(commands = ['sql'])
def sql_try(message):
    m_id = message.chat.id
    query = f'SELECT user_n_id FROM "USER_NAME" WHERE user_n_name = \'SAOP\''
    cursor.execute(query)
    # fetchall это метод который хранит данные которые пришли с запроса 
    resoult = cursor.fetchall()
    bot.send_message(m_id,resoult)


def get_category(message_3):
    user_category = message_3.text 
    print(user_category)

def get_id(message_2):
    id_user = message_2.text
    print(id_user)
    y = bot.send_message(message_2,'Id saved successfully')
    bot.register_next_step_handler(y,input_category)
    cursor.execute('INSERT INTO "CATEGORY" (user_id, cat_name)\
        VALUES (%s, %s)'.format(id_cat[0].split,id_cat[1]))
    c = cursor.fetchall()
    connection.commit()
    bot.send_message(message_2.chat.id,c)



if __name__ == '__main__': 
    while True:
        try:
            bot.infinity_polling(True)
        except Exception:
            time.sleep(15)



@bot.message_handler(commands=['start'])
def welcome_func(message):
    n
    bot.register_next_step_handler(wlcm,name_of_user)

def name_of_user(message):
    try:
        user_id = message.from_user.id
        user_data[user.id] = User(message.text)
        wlcm = bot.send_message(message.chat.id,'Hey!,  if u want to login please enter your parol from app:')
        bot.register_next_step_handler(message.chat.id,)
    except Exception as e:
        bot.send_message(message,'User undefined')

def name_of_parol(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]

bot.enable_save_next_step_handlers(delay = 2)

bot.load_next_step_handlers()



class User:
    def __init__(self,name,parol):
        self.name = name 
        self.parol = parol

@bot.message_handler(commands=['name'])
def welcome_func(query:Message):
    try:
        step_1 = 
        a = bot.register_next_step_handler(step_1, set_name)
    print(a)

def set_name(message):
    try:
        name = message.text
        check_user = cursor.execute(f"SELECT user_n_name FROM \"USER_NAME\"")

        bot.send_message(check_user,message.chat.id,(f'Ваше имя {name}'))
    except Exception as e:
        bot.send_message(message.chat.id,f'column {name} does not exist')