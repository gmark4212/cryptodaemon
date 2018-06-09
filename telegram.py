#!/usr/bin/python
# -*- coding: utf-8 -*-
import telebot
from telebot import types

TOKEN = '567981171:AAE0yeFOkKUqGs00SILkFDrbP8m8wcCqIcs'

bot = telebot.TeleBot(TOKEN)

markup = types.ReplyKeyboardMarkup(row_width=1)
btn_start = types.KeyboardButton('запустить CryptoBot')
btn_stop = types.KeyboardButton('остановить CryptoBot')
btn_help = types.KeyboardButton('help')
markup.add(btn_start, btn_stop, btn_help)


markup_inline_start = types.InlineKeyboardMarkup(row_width=2)
btn_fetch_balance = types.InlineKeyboardButton('Текущий баланс',
                                               callback_data='CryptoBot.fetch_balance()')
btn_fetch_order = types.InlineKeyboardButton('Текущий ордер',
                                             callback_data='CryptoBot.fetch_order()')
btn_create_order = types.InlineKeyboardButton('Создать ордер',
                                              callback_data='CryptoBot.create_order()')
btn_fetch_open_orders = types.InlineKeyboardButton('Проверить открытые ордера',
                                                   callback_data='CryptoBot.fetch_my_open_orders()')
markup_inline_start.add(btn_fetch_balance, btn_fetch_order, btn_create_order, btn_fetch_open_orders)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, 'Hello', reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == 'запустить CryptoBot':
        # CryptoBot.start_trading()
        bot.reply_to(message, 'CryptoBot.start_trading()', reply_markup=markup_inline_start)
    elif message.text == 'остановить CryptoBot':
        # CryptoBot.stop_trading()
        bot.reply_to(message, 'CryptoBot.stop_trading()', reply_markup=markup)
    else:
        bot.reply_to(message, 'Hello', reply_markup=markup)


@bot.callback_query_handler(func= lambda call: True)
def call_back(call):
    if call.data == 'CryptoBot.fetch_balance()':
        bot.reply_to(call.message, text='Ваш баланс: ', reply_markup=markup_inline_start)
    elif call.data == 'CryptoBot.fetch_order()':
        bot.reply_to(call.message, text='Ваш текущий ордер: ', reply_markup=markup_inline_start)
    elif call.data == 'CryptoBot.create_order()':
        bot.reply_to(call.message, text='Создать ордер ', reply_markup=markup_inline_start)
    elif call.data == 'CryptoBot.fetch_my_open_orders()':
        bot.reply_to(call.message, text='Oткрытые ордера: ', reply_markup=markup_inline_start)
    

bot.polling()



# class TelegramBot:
#     pass

