#!usr/bin/python3

__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import requests
import os
import sys
import argparse
import telegram
import google.auth
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from dotenv import load_dotenv
from my_logger import get_logger
from detect_intent import detect_intent_text


def start(bot, update):
    logger.debug('start вроде бы')
    bot.sendMessage(
        chat_id=update.message.chat_id, 
        text="start_handler: Здравствуйте. Задавайте Ваш вопрос.",
        )


def send_text_message(bot, update):
    credentials, project = google.auth.default()
    chat_id = update.message.chat_id
    language_code = 'ru-RU'
    text = update.message.text

    logger.debug('Новое сообщение:')
    logger.debug('Для меня от: {}'.format(chat_id))
    logger.debug('Текст:{}\n'.format(event.text))

    query_result = detect_intent_text(project, user_id, text, language_code)
    bot.sendMessage(chat_id, query_result.fulfillment_text)


def main():
    # init
    logger = get_logger('bot_tg')

    load_dotenv()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-credentials.json'
    credentials, project = google.auth.default()

    telegram_token = os.getenv("TELEGRAM_TOKEN")

    # если нужно запустить через socks5 proxy:
    # pp = telegram.utils.request.Request(proxy_url='socks5h://51.158.68.133:8811')
    # bot = telegram.Bot(token=telegram_token, request=pp)

    # без socks5 proxy:
    bot = telegram.Bot(token=telegram_token)

    updater = Updater(token=telegram_token, use_context=True)

    # do
    start_handler = CommandHandler('start', start)
    updater.dispatcher.add_handler(start_handler)

    text_massage_handler = MessageHandler(Filters.text, send_text_message)
    updater.dispatcher.add_handler(text_massage_handler)

    logger.debug('все готово')

    try:
        logger.debug('start_polling')
        updater.start_polling()
        logger.debug('polling упал?')
    except Exception as err:
        print('все пропало')
        print(err)
    # except KeyboardInterrupt:
    #     logger.info('Бот остановлен')
    # except Exception  as err:
    #     logger.error('Бот упал с ошибкой:')
    #     logger.error(err)
    #     logger.debug(err, exc_info=True)
    # print('чего-то ждем?')

    # Останавливаем бота, если были нажаты Ctrl + C
    # updater.idle()


if __name__ == "__main__":
    main()
