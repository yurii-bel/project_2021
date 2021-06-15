import telebot
import psycopg2
import os
import configparser

# Getting  token of telegram bot and data that we need for connect, from environment heroku
# if this file is run in Heroku, we get data from configuration file in another way. 
try:
    BOT_TOKEN = os.environ['BOT_TOKEN']
    DATABASE_URL = os.environ['DATABASE_URL']
    connection = psycopg2.connect(DATABASE_URL)
except KeyError:
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8-sig')
    BOT_TOKEN = config.get('Bot', 'bot_token_sasha')
    connection = psycopg2.connect(database=config.get('PostgreSql', 'database'),
                                  user=config.get('PostgreSql', 'user'),
                                  password=config.get('PostgreSql', 'password'),
                                  host=config.get('PostgreSql', 'host'))

# Connect our bot. 
bot = telebot.TeleBot(BOT_TOKEN)

# For add, select or delete something from data base.
cursor = connection.cursor()

# Was functions can getting accses from our variables from the outside.
user_n_name = None
user_n_id = None
user_p_password = None
user_p_id = None
user_id = None
cat_name = None

# Welcome.
@bot.message_handler(commands=['start'])
def hello_user(message):
    bot.send_message(message.chat.id,'Приветствую, я помошник бот для приложения TimeSoft пожалуйста если\
         вы хотите пользоваться мной введите команду /login')

# Ask the user to log in. 
@bot.message_handler(commands=['login'])
def login_me(message):
    bot.send_message(message.from_user.id, 'Если вы зарегистрированы в приложениии\
         TimeSoft введите свое имя: ')
    bot.register_next_step_handler(message,info_of_user)

# From name of the user -  we will get all info from data of base.
def info_of_user(message):
    global user_n_name
    global user_n_id
    global user_id
    global user_p_id
    global user_p_password

    cursor.execute(f"SELECT user_n_id FROM \"USER_NAME\" WHERE user_n_name = '{message.text}'")
    user_n_id = cursor.fetchall()
    if user_n_id:
        user_n_id = user_n_id[0][0]
        user_n_name = message.text
        
        cursor.execute(f"SELECT user_p_id FROM \"USER\" WHERE user_n_id = '{user_n_id}'")
        user_p_id = cursor.fetchall()
        if user_p_id:
            user_p_id = user_p_id[0][0]

        cursor.execute(f"SELECT user_id FROM \"USER\" WHERE user_n_id = '{user_n_id}'")
        user_id = cursor.fetchall()
        if user_id:
            user_id = user_id[0][0]

        cursor.execute(f"SELECT user_p_password FROM \"USER_PRIVATE\" WHERE user_p_id = '{user_p_id}'")
        user_p_password = cursor.fetchall()
        if user_p_password:
            user_p_password = user_p_password[0][0]

        bot.send_message(message.chat.id,'Отлично имя верное, теперь введите пароль: ')
        bot.register_next_step_handler(message,password_of_user)
    else: bot.send_message(message.chat.id,'Такого логина не существует, пожалуйста зарегистрируйтесь в приложениии')

# If entered  password is equal with password from data of base then , we are updating our telegram id of the user.
def password_of_user(message):
    global user_p_password
    global user_n_id
    global user_n_name
    global user_id
    global user_p_id

    if message.text == user_p_password:
        cursor.execute(f"UPDATE \"USER_NAME\" SET user_n_telegram = '{message.from_user.id}' WHERE user_n_id = '{user_n_id}'" )
        connection.commit()
        bot.send_message(message.chat.id,'Вы авторизированы успешно!, для добавления\
                        новой активности или же изменения текущей find_activity  :')
    else:
        user_n_name = None
        user_n_id = None
        user_id = None
        user_p_id = None
        user_p_password = None
        bot.send_message(message.chat.id,'Указан неверный пароль')
        bot.register_next_step_handler(message, add_activity)

# Funktion add activity
bot.message_handler(content_types=['text'])
def add_activity(message):
    global user_id
    global cat_name
    if message.text == 'find_activity':
        bot.send_message(message.chat.id,'Добавте  свою, или же введите существующую категорию :')
        cursor.execute(f"SELECT cat_name FROM \"CATEGORY\" WHERE user_id = {user_id} ")
        cat_name = cursor.fetchall()
        if cat_name:
            cat_name[0][0]
            print(cat_name)



    



    
if __name__ == '__main__':
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            print(e)
