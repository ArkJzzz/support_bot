#!usr/bin/python3

import requests
import os
import sys
import argparse
import logging
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from detect_intent import detect_intent_text


def start(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id, 
        text="start_handler: Здравствуйте.",
        )


def textMessage(bot, update):
    credentials, project = google.auth.default()
    chat_id = update.message.chat_id
    language_code = 'ru-RU'
    text = update.message.text

    fulfillment_text = detect_intent.detect_intent_text(project, chat_id, text, language_code)

    logging.debug('Message text: {}\n'.format(text))
    logging.debug('Fulfillment text: {}\n'.format(fulfillment_text))
    
    bot.sendMessage(chat_id, fulfillment_text)


def main():
    # init
    logging.basicConfig(
        format = u'[LINE:%(lineno)d]#  %(message)s', 
        level = logging.DEBUG,
        )

    load_dotenv()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'df_key.json'
    credentials, project = google.auth.default()

    telegram_token = os.getenv("TELEGRAM_TOKEN")
    bot = telegram.Bot(token=telegram_token)
    updater = Updater(token=telegram_token)

    # do
    start_handler = CommandHandler('start', start)
    updater.dispatcher.add_handler(start_handler)

    text_massage_handler = MessageHandler(Filters.text, textMessage)
    updater.dispatcher.add_handler(text_massage_handler)

    updater.start_polling()

    # Останавливаем бота, если были нажаты Ctrl + C
    updater.idle()


if __name__ == "__main__":
    main()
