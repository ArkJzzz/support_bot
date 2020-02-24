#!usr/bin/python3

__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import requests
import os
import sys
import argparse
import logging
from logging.handlers import RotatingFileHandler
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
import google.auth
from dotenv import load_dotenv
from detect_intent import detect_intent_text


logger = logging.getLogger('bot_tg')

logging.basicConfig(
    format='%(asctime)s %(name)s - %(funcName)s:%(lineno)d - %(message)s', 
    datefmt='%Y-%b-%d %H:%M:%S (%Z)',
    )


def start(update, context):
    chat_id=update.effective_chat.id
    text='start_handler: Здравствуйте. Задавайте Ваш вопрос.'

    context.bot.send_message(chat_id, text)

    logger.debug('start_handler')


def send_text_message(update, context):
    credentials, project = google.auth.default()

    chat_id = update.effective_chat.id
    username = update.effective_chat.username
    language_code = 'ru-RU'
    text = update.message.text
    
    query_result = detect_intent_text(project, chat_id, text, language_code)
    answer = query_result.fulfillment_text

    context.bot.send_message(chat_id, answer)

    logger.debug('Новое сообщение:')
    logger.debug('Для меня от {}, chat_id {}'.format(username, chat_id))
    logger.debug('Текст: {}'.format(text))
    logger.debug('Detect Intent: {}'.format(query_result.intent.display_name))
    logger.debug('Ответ: {}\n'.format(answer))



def main():
    # init

    logger.setLevel(logging.DEBUG)

    load_dotenv()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-credentials.json'
    credentials, project = google.auth.default()

    telegram_token = os.getenv("TELEGRAM_TOKEN")

    # если нужно запустить через socks proxy:
    proxy_url = os.getenv('PROXY_URL')
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    REQUEST_KWARGS={
        'proxy_url': proxy_url,
        # Optional, if you need authentication:
        'urllib3_proxy_kwargs': {
            'assert_hostname': 'False',
            # 'cert_reqs': 'CERT_NONE'
            'cert_reqs': 'CERT_REQUIRED',
            # 'username': username,
            # 'password': password
        }
    }



    updater = Updater(
        token=telegram_token, 
        use_context=True, 
        #request_kwargs=REQUEST_KWARGS,
    )

    # do
    start_handler = CommandHandler('start', start)
    updater.dispatcher.add_handler(start_handler)

    text_massage_handler = MessageHandler(Filters.text, send_text_message)
    updater.dispatcher.add_handler(text_massage_handler)

    logger.debug('все готово')

    try:
        updater.start_polling()

    except telegram.error.NetworkError:
        logger.error('Не могу подключиться к telegram')
    except Exception  as err:
        logger.error('Бот упал с ошибкой:')
        logger.error(err)
        logger.debug(err, exc_info=True)

    updater.idle()
    logger.info('Бот остановлен') 

if __name__ == "__main__":
    main()
