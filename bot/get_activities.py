import telebot 
import psycopg2
import configparser
import os



config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')



try:
    BOT_TOKEN = os.environ['BOT_TOKEN']
except Exception:
    TOKEN = config.get('Bot', 'bot_token_actvs')

bot = telebot.TeleBot(TOKEN)

connection = psycopg2.connect(database=config.get('PostgreSql', 'database'),
                              user=config.get('PostgreSql', 'user'),
                              password=config.get('PostgreSql', 'password'),
                              host=config.get('PostgreSql', 'host'))
cursor = connection.cursor()


def previous_check():
    cursor.execute('SELECT user_id FROM \'USER\' WHERE user_n_name = {message.from_user.id}'  )
    



@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Если вы хотите авторизировать себя , то нажмите на  комманду /login' )

# @bot.message_handler(commands = ['\login'])
