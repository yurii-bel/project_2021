# Подключаем библиотеку telebot для работы с телеграм ботом.
import telebot

# Идентифицируем телеграм бота.
bot = telebot.TeleBot('1891194594:AAGDaHHTuZv5mDBIV8Q4Sjd7xU1RPPry0ns')


# Отслеживаем ввод текста для того, что бы ответить что-то умное.
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """[summary]

    Args:
        message ([type]): [description]
    """
    # Отвечаем комментарием.
    bot.reply_to(
        message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')


# Отслеживаем тип сообщения, что бы ответить.
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """[summary]

    Args:
        message ([type]): [description]
    """
    # Обычный тип ответа.
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')


# Задаём боту непрерывное отслеживание новых сообщений. Если бот упадёт, а
# сообщения продолжат поступать, они будут накапливаться в течение 24 часов
# на серверах Telegram, и в случае восстановления бота прилетят ему все сразу.
bot.polling(none_stop=True)
