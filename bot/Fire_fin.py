import telebot
from telebot.types import User
import psycopg2 as db
from psycopg2 import sql
import time

tk = '1891194594:AAGDaHHTuZv5mDBIV8Q4Sjd7xU1RPPry0ns'




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
            'Time_soft' across comand '/log_name', '/log_id'")



@bot.message_handler(commands=['log_name'])
def input_log_name(message_n):
    name = bot.send_message(message_n.chat.id,'Please input your name from app "Time-soft":')
    user_n = message_n.text
    bot.send_message(message_n.chat.id,f'your name is added {user_n}')



@bot.message_handler(commands=['log_id'])
def input_log_name(message_id):
    id = bot.send_message(message_id.chat.id,'Please input your id from app "Time-soft":')
    bot.send_message(message_id,f'your name is added {id}')




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
    



#@bot.message_handler(commands = ['sql'])
# def sql_try(message):
#     m_id = message.chat.id
#     query = f'SELECT user_n_id FROM "USER_NAME" WHERE user_n_name = \'SAOP\''
#     cursor.execute(query)
#     # fetchall это метод который хранит данные которые пришли с запроса 
#     resoult = cursor.fetchall()
#     bot.send_message(m_id,resoult)


# def get_category(message_3):
#     user_category = message_3.text 
#     print(user_category)

# def get_id(message_2):
#     id_user = message_2.text
#     print(id_user)
#     y = bot.send_message(message_2,'Id saved successfully')
#     bot.register_next_step_handler(y,input_category)
#     # cursor.execute('INSERT INTO "CATEGORY" (user_id, cat_name)\
#     #     VALUES (%s, %s)'.format(id_cat[0].split,id_cat[1]))
#     # c = cursor.fetchall()
#     # connection.commit()
#     # bot.send_message(message_2.chat.id,c)



if __name__ == '__main__': 
    while True:
        try:
            bot.infinity_polling(True)
        except Exception:
            time.sleep(15)

