#!usr/bin/python3

"""
Module Docstring
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'ArkJzzz (arkjzzz@gmail.com)'

import requests
import os
import sys
import argparse
import telegram
import logging
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv



def start(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Здравствуйте.")


def echo(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)


def main():
    # init
    load_dotenv()
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    bot = telegram.Bot(token=telegram_token)
    updater = Updater(token=telegram_token)

    # do
    start_handler = CommandHandler('start', start)
    updater.dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text, echo)
    updater.dispatcher.add_handler(echo_handler)

    updater.start_polling()


if __name__ == "__main__":
    main()
