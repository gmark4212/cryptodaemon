#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import requests
import telebot
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode
from telebot import TeleBot, types
from cryptobot import CryptoBot
from strategy import Strategy
from storage import *
from config import *

bot = TeleBot(TOKEN)
users = {}


@bot.message_handler(commands=['start'], content_types='text')
def command_start(message):
    # Отправляет на веб-сервер POST запрос
    data = {'id': message.chat.id, 'action': message.text}
    requests.post('http://httpbin.org/post', json.dumps(data))
    if chatId not in users:
        # спрашивает имя и отправляет на следующий этап регистрации - секретный ключ
        bot.send_message(message.chat.id, "Hello! I am Bot.\nWhat is you name?")
        bot.register_next_step_handler(message, process_NAME_step)
        # иначе
    else:
        # приветствует
       bot.send_message(message.chat.id, f"Welcome, {message.text}!")


def process_NAME_step(message):
    "запрашивает секретный ключ"
    # раннее полученное имя сохраняет
    users[message.chat.id] = message.text
    bot.send_message(message.chat.id, 'SECRET KEY: ')
    bot.register_next_step_handler(message, process_SECRET_step)


def process_SECRET_step(message):
    "проверяет правильно ли пользователь ввел код"
    # если все гуд
    if message.text == 'secret':
        # приветствует и предоставляет информацию от командах
        bot.send_message(message.chat.id, f"Welcome, {users[message.chat.id]}!")
        command_help(message)
    else:
        # в случае неправильного ввода опять запрашивает ключ
        bot.send_message(message.chat.id, 'SECRET KEY: ')
        bot.register_next_step_handler(message, process_SECRET_step)


@bot.message_handler(commands=['help'])
def command_help(message):
    msg = text(bold('Доступны следующие команды: \n'),
               '/start - при запуске ТелеграмБота необходимо\n ввести свое имя и секретный ключ\n',
               '/help - Предоставляет информацию о доступных командах\n',
               '/run - Запускает CryptoBot\n',
               '/balance - Предоставляет информацию о текущем балансе\n',
               '/stop - Останавливает CryptoBot')
    bot.send_message(message.chat.id, msg, parse_mode=ParseMode.MARKDOWN)

@bot.message_handler(commands=['run'])
def run_cryptobot(message):
    "запусткает криптобот и сообщает об этом "
    try:
        cryptobot = CryptoBot(Strategy(), emulation_mode=True)
        cryptobot.start_trading()
    except KeyError:
        pass
    bot.send_message(message.chat.id, 'CryptoBot запущен')


@bot.message_handler(commands=['balance'])
def balance(message):
    "выводит информацию о текущем балансе"
    try:
        cryptobot = CryptoBot(Strategy(), emulation_mode=True)
        fetch_balance = cryptobot.fetch_balance()
    except Exception:
        pass
    else:
        bot.send_message(message.chat.id, f'Ваш баланс: {fetch_balance}')


@bot.message_handler(commands=['stop'])
def stop_cryptobot(message):
    "останавлявает криптобот и сообщает об этом"
    try:
        cryptobot = CryptoBot(Strategy(), emulation_mode=True)
        cryptobot.stop_trading()
    except Exception:
        pass
    else:
        bot.send_message(message.chat.id, 'CryptoBot остановлен')
        data = {'id': message.chat.id, 'action': message.text}
        requests.post('http://httpbin.org/post', json.dumps(data))



bot.polling(none_stop=True)







