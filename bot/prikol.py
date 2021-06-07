import time

import telebot
from telebot import types

TOKEN = '1887201750:AAH9nOU0FmKm3j5IBDhgwtHNhqknQJanVjk'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    bot.send_message(cid, "здарова, работяги")


bot.polling()