#!/usr/bin/python
# -*- coding: utf-8 -*-
import telebot

TOKEN = '567981171:AAE0yeFOkKUqGs00SILkFDrbP8m8wcCqIcs'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome!')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.polling()

# class TelegramBot:
#     pass

