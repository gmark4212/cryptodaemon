#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import telebot
from telebot import types
from cryptobot import CryptoBot
from strategy import Strategy
from storage import *
from config import *

cryptobot = CryptoBot(Strategy(), '-e' in sys.argv)
bot = telebot.TeleBot(TOKEN)


markup = types.ReplyKeyboardMarkup()
bt_balance = types.KeyboardButton('Текущий баланс')
bt_order = types.KeyboardButton('Текущий ордер')
bt_open_order = types.KeyboardButton('Все открытые ордера')
markup.row(bt_balance, bt_order)
markup.row(bt_open_order)
hidden_markup = types.ReplyKeyboardRemove()

users = {}

# обрабатывать команду «/ start»
@bot.message_handler(commands=['start'])
def command_start(message):
    chat_id = message.chat.id
    name = message.text
    if chat_id not in users:
        bot.send_message(chat_id, "Hello! I am Bot. What is you name?")
        bot.register_next_step_handler(message, process_API_step)
    else:
        bot.send_message(chat_id, "Welcome, {}!".format(name))


def process_API_step(message):
    chat_id = message.chat.id
    name = message.text
    users[chat_id] = name
    bot.send_message(chat_id, 'API: ')
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


orders = []
@bot.message_handler(func=lambda message: True)
def get(message):
    if message.text == 'Текущий баланс':
        fetch_balance = cryptobot.fetch_balance()
        bot.send_message(message.chat.id, 'Ваш баланс: {}'.format(fetch_balance), reply_markup=markup)

    elif message.text == 'Текущий ордер':
        for order in orders:
            if order['id'] == message.chat.id:
                responce = cryptobot.exchange.fetch_order(oid=order['id']['status'])
                bot.send_message(message.chat.id, 'Текущий ордер: {}'.format(responce), reply_markup=markup)
            else:
                bot.send_message(message.chat.id, 'Текущий ордер: {}'.format(None), reply_markup=markup)

    elif message.text == 'Все открытые ордера':
            for order in orders:
                if order['status'] == 'open':
                    bot.send_message(message.chat.id, 'Oткрытые ордера: {}'.format(order), reply_markup=markup)
                else:
                    bot.send_message(message.chat.id, 'Oткрытые ордера: {}'.format(None), reply_markup=markup)



bot.polling()



# class TelegramBot:
#     pass

