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

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome!')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.polling()

# class TelegramBot:
#     pass

