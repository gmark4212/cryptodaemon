import telebot
from telebot.types import Message
import time
from config_telebot import *


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])  # Если команда /start - отправляем сообщение из файла config.py
def command_handler(message: Message):
    bot.send_message(message.chat.id, STARTMESSAGE)


@bot.message_handler(commands=['about'])  # Если команда /about - отправляем сообщение из файла config.py
def command_handler(message: Message):
    bot.send_message(message.chat.id, ABOUT)


@bot.message_handler(commands=['help'])  # Если команда /help - отправляем сообщение из файла config.py
def command_handler(message: Message):
    bot.send_message(message.chat.id, HELPMESSAGE)


@bot.message_handler(content_types=['text'])
def delay_handler(message: Message):
    pass  # Необходимо добавить шаблоны сообщений

if __name__ == '__main__':
    bot.polling()
