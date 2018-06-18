#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import telebot
from telebot import TeleBot, types
from cryptobot import CryptoBot
from strategy import Strategy
from storage import *
from config import *


class TelegramBot(TeleBot):

    def __init__(self, TOKEN):
        super().__init__(token=TOKEN)
        self.token = TOKEN
        self.users = {}
        self.cryptobot = CryptoBot(Strategy(), emulation_mode=True)


if __name__ == '__main__':

    bot = TelegramBot(TOKEN)


    @bot.message_handler(commands=['start'])
    def start(message):
        "проверяет, обращался ли пользователь к нему раньше"
        chatId = message.chat.id
        text = message.text
        # если пользователя нет в users
        if chatId not in bot.users:
            # спрашивает имя и отправляет на следующий этап регистрации - секретный ключ
            bot.send_message(chatId, "Hello! I am Bot. What is you name?")
            bot.register_next_step_handler(message, process_NAME_step)
            # иначе
        else:
            # приветствует
            bot.send_message(chatId, "Welcome, {}!".format(text))

    def process_NAME_step(message):
        "запрашивает секретный ключ"
        chatId = message.chat.id
        name = message.text
        # раннее полученное имя сохраняет
        bot.users[chatId] = name
        bot.send_message(chatId, 'SECRET KEY: ')
        bot.register_next_step_handler(message, process_SECRET_step)


    def process_SECRET_step(message):
        "проверяет правильно ли пользователь ввел код"
        chatId = message.chat.id
        SECRET = message.text
        #если все гуд
        if SECRET == 'secret':
            # приветствует и предоставляет информацию от командах
            bot.send_message(chatId, "Welcome, {}!".format(bot.users[chatId]))
            command_help(message)
        else:
            # в случае неправильного ввода опять запрашивает ключ
            bot.send_message(chatId, 'SECRET KEY: ')
            bot.register_next_step_handler(message, process_SECRET_step)


    @bot.message_handler(commands=['help'])
    def command_help(message):
        "выводит сообщение о доступных коммандах и что они могут"
        cid = message.chat.id
        help_text =  " Доступны следующие команды: \n"
        for key in COMMANDS:
            help_text += "/" + key + ": " + COMMANDS[key] + "\n"
            bot.send_message(cid, help_text)


    @bot.message_handler(commands=['run'])
    def run_cryptobot(message):
        "запусткает криптобот и сообщает об этом "
        bot.cryptobot.start_trading()
        chatId = message.chat.id
        bot.send_message(chatId, 'CryptoBot запущен')


    @bot.message_handler(commands=['stop'])
    def stop_cryptobot(message):
        "останавлявает криптобот и сообщает об этом"
        bot.cryptobot.keep_working = False
        bot.cryptobot.stop_trading()
        chatId = message.chat.id
        bot.send_message(chatId, 'CryptoBot остановлен')


    @bot.message_handler(commands=['balance'])
    def balance(message):
        "выводит информацию о текущем балансе"
        fetch_balance = bot.cryptobot.fetch_balance()
        bot.send_message(message.chat.id, 'Ваш баланс: {}'.format(fetch_balance))


    bot.polling(none_stop=True)







