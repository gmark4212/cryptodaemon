#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import telebot
from telebot import types
from cryptobot import CryptoBot
from strategy import Strategy
from storage import *
from config import *


class TelegramBot(telebot.TeleBot):

    def __init__(self, ):
        super().__init__(TOKEN)
        self.db = BotDataStorage()
        self.users = {}
        self.orders = []
        self.cryptobot = CryptoBot(Strategy(), '-e' in sys.argv)

    def markup(self):
        self.markup = types.ReplyKeyboardMarkup()
        self.bt_balance = types.KeyboardButton('Текущий баланс')
        self.bt_order = types.KeyboardButton('Текущий ордер')
        self.bt_open_order = types.KeyboardButton('Все открытые ордера')
        self.markup.row(self.bt_balance, self.bt_order)
        self.markup.row(self.bt_open_order)
        return markup

    def hidden(self):
        hidden_markup = types.ReplyKeyboardRemove()
        return hidden_markup

if __name__ == '__main__':

    bot = TelegramBot()
    bot.polling()

    @bot.message_handler(commands=['start'])
    def start(message):
        chatId = message.chat.id
        text = message.text
        bot.users[chatId] = text
        if chatId not in bot.users:
            bot.send_message(chatId, "Hello! I am Bot. What is you name?")
            bot.register_next_step_handler(message, process_API_step)
        else:
            bot.send_message(chatId, "Welcome, {}!".format(text))

    def process_API_step(message):
        chatId = message.chat.id
        name = message.text
        users[chatId] = name
        bot.send_message(chatId, 'API: ')
        bot.register_next_step_handler(message, process_SECRET_step)

    def process_SECRET_step(message):
        chat_id = message.chat.id
        API = message.text
        if API == 'api':
            bot.send_message(chat_id, 'SECRET KEY: ')
            bot.register_next_step_handler(message, process_last_step)
        else:
            bot.send_message(chat_id, 'API:')
            bot.register_next_step_handler(message, process_API_step)

    def process_last_step(message):
        chat_id = message.chat.id
        SECRET = message.text
        if SECRET == 'secret':
            bot.send_message(chat_id, "Welcome, {}!".format(users[chat_id]))
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
    def run_cryptobot(message):
        try:
            bot.send_message(message.chat.id, 'CryptoBot запущен', reply_markup=markup)
            cryptobot.start_trading()
        except TypeError:
            bot.send_message(message.chat.id, 'Error..')


    @bot.message_handler(commands=['stop'])
    def stop_cryptobot(message):
        try:
            bot.send_message(message.chat.id, 'CryptoBot остановлен', reply_markup=hidden_markup)
            cryptobot.stop_trading()
        except Exception:
            bot.send_message(message.chat.id, 'Error..')



    @bot.message_handler(func=lambda message: True)
    def get(message):
        if message.text == 'Текущий баланс':
            fetch_balance = cryptobot.fetch_balance()
            bot.send_message(message.chat.id, 'Ваш баланс: {}'.format(fetch_balance), reply_markup=markup)

        elif message.text == 'Текущий ордер':
            for order in bot.orders:
                if order['id'] == message.chat.id:
                    responce = cryptobot.exchange.fetch_order(oid=order['id']['status'])
                    bot.send_message(message.chat.id, 'Текущий ордер: {}'.format(responce), reply_markup=markup)
                else:
                    bot.send_message(message.chat.id, 'Текущий ордер: {}'.format(None), reply_markup=markup)

        elif message.text == 'Все открытые ордера':
                for order in bot.orders:
                    if order['status'] == 'open':
                        bot.send_message(message.chat.id, 'Oткрытые ордера: {}'.format(order), reply_markup=markup)
                    else:
                        bot.send_message(message.chat.id, 'Oткрытые ордера: {}'.format(None), reply_markup=markup)









