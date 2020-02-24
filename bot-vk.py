#!usr/bin/python3

__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import os
import logging
import google.auth
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
from dotenv import load_dotenv
from detect_intent import detect_intent_text

logger = logging.getLogger('bot_vk')

logging.basicConfig(
    format='%(asctime)s %(name)s - %(funcName)s:%(lineno)d - %(message)s', 
    datefmt='%Y-%b-%d %H:%M:%S (%Z)',
    )



def send_text_message(event, vk):
    credentials, project = google.auth.default()
    user_id = event.user_id
    language_code = 'ru-RU'
    text = event.text

    query_result = detect_intent_text(project, user_id, text, language_code)

    logger.info('Detect Intent: {}\n'.format(query_result.intent.display_name))

    if query_result.intent.is_fallback != True: #FIXME: отловить флаг 'fallback'
	    vk.messages.send(
	        user_id = user_id,
	        message = query_result.fulfillment_text,
	        random_id = random.randint(1,1000)
	    )
    

def main():

    # init
    logger.setLevel(logging.DEBUG)

    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-credentials.json'
    credentials, project = google.auth.default()

    vk_session = vk_api.VkApi(token=vk_token) 
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    logger.debug('все готово')

    # do

    try:

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                logger.debug('Новое сообщение:')
                logger.debug('Для меня от: {}'.format(event.user_id))
                logger.info('Текст:{}'.format(event.text))
                send_text_message(event, vk)
    except KeyboardInterrupt:
        logger.info('Бот остановлен')
    except Exception  as err:
        logger.error('Бот упал с ошибкой:')
        logger.error(err)
        logger.debug(err, exc_info=True)
            

if __name__ == "__main__":
    main()