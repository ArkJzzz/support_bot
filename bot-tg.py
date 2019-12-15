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
    logger.debug('Ответ: {}\n'.format(answer))


def main():
    # init
    logger = get_logger('bot_tg')

    load_dotenv()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-credentials.json'
    credentials, project = google.auth.default()

    telegram_token = os.getenv("TELEGRAM_TOKEN")

    # если нужно запустить через socks proxy:
    REQUEST_KWARGS={
        'proxy_url': 'socks4://171.103.9.22:4145/',
        # Optional, if you need authentication:
        'urllib3_proxy_kwargs': {
            'assert_hostname': 'False',
            'cert_reqs': 'CERT_NONE'
            # 'username': 'user',
            # 'password': 'password'
        }
    }

    updater = Updater(token=telegram_token, use_context=True, request_kwargs=None)

    # do
    start_handler = CommandHandler('start', start)
    updater.dispatcher.add_handler(start_handler)

    text_massage_handler = MessageHandler(Filters.text, send_text_message)
    updater.dispatcher.add_handler(text_massage_handler)

    logger.debug('все готово')

    try:
        updater.start_polling()

    except Exception as err:
        print('все пропало')
        print(err)
    except KeyboardInterrupt:
        logger.info('Бот остановлен')
    except Exception  as err:
        logger.error('Бот упал с ошибкой:')
        logger.error(err)
        logger.debug(err, exc_info=True)

    updater.idle()
    logger.info('Бот остановлен') 

if __name__ == "__main__":
    main()
