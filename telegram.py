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

    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    bt_run = types.KeyboardButton('Запустить CryptoBot')
    bt_balance = types.KeyboardButton('Текущий баланс')
    bt_stop_order = types.KeyboardButton('Остановить CryptoBot')
    keyboard.add(bt_run, bt_balance, bt_stop_order)
    hidden_keyboard = types.ReplyKeyboardRemove()

    @bot.message_handler(commands=['start'])
    def start(message):
        chatId = message.chat.id
        text = message.text
        if chatId not in bot.users:
            bot.send_message(chatId, "Hello! I am Bot. What is you name?")
            bot.register_next_step_handler(message, process_API_step)
        else:
            bot.send_message(chatId, "Welcome, {}!".format(text), reply_markup=keyboard)

    def process_API_step(message):
        chatId = message.chat.id
        name = message.text
        bot.users[chatId] = name
        bot.send_message(chatId, 'API: ')
        bot.register_next_step_handler(message, process_SECRET_step)

    def process_SECRET_step(message):
        chatId = message.chat.id
        API = message.text
        if API == 'api':
            bot.send_message(chatId, 'SECRET KEY: ')
            bot.register_next_step_handler(message, process_last_step)
        else:
            bot.send_message(chatId, 'API:')
            bot.register_next_step_handler(message, process_API_step)

    def process_last_step(message):
        chatId = message.chat.id
        SECRET = message.text
        if SECRET == 'secret':
            bot.send_message(chatId, "Welcome, {}!".format(bot.users[chatId]))
            command_help(message)
        else:
            bot.send_message(chat_id, 'SECRET KEY: ')
            bot.register_next_step_handler(message, process_SECRET_step)


    @bot.message_handler(commands=['help'])
    def command_help(message):
        cid = message.chat.id
        help_text =  " Доступны следующие команды: \n"
        for key in COMMANDS:
            help_text += "/" + key + ": "
            help_text += COMMANDS[key] + "\n"
            bot.send_message(cid, help_text)


    @bot.message_handler(commands=['run'])
    @bot.message_handler(func=lambda message: True)
    def run_cryptobot(message):
        if message.text == '/run' or message.text == 'Запустить CryptoBot':
            bot.send_message(message.chat.id, 'CryptoBot запущен', reply_markup=keyboard)
            bot.cryptobot.start_trading()


    @bot.message_handler(commands=['stop'])
    @bot.message_handler(func=lambda message: True)
    def stop_cryptobot(message):
        if message.text == '/stop' or message.text == 'Остановить CryptoBot':
            cryptobot.stop_trading()
            bot.send_message(message.chat.id, 'CryptoBot остановлен', reply_markup=hidden_keyboard)


    @bot.message_handler(func=lambda message: True)
    def balance(message):
        if message.text == 'Текущий баланс':
            fetch_balance = bot.cryptobot.fetch_balance()
            bot.send_message(message.chat.id, 'Ваш баланс: {}'.format(fetch_balance), reply_markup=keyboard)


    bot.polling()







