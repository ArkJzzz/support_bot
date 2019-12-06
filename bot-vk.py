#!usr/bin/python3

__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import os
import google.auth
import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from my_logger import get_logger
from detect_intent import detect_intent_text


def send_text_message(event, vk):
    credentials, project = google.auth.default()
    user_id = event.user_id
    language_code = 'ru-RU'
    text = event.text

    query_result = detect_intent_text(project, user_id, text, language_code)

    if query_result.intent.display_name != 'Default Fallback Intent':
	    vk.messages.send(
	        user_id = user_id,
	        message = query_result.fulfillment_text,
	        random_id = random.randint(1,1000)
	    )
    

def main():

    # init
    logger = get_logger('bot_vk')

    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'df_key.json'
    credentials, project = google.auth.default()

    vk_session = vk_api.VkApi(token=vk_token)    
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    # do
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            logger.debug('Новое сообщение:')
            logger.debug('Для меня от: {}'.format(event.user_id))
            logger.info('Текст:{}\n'.format(event.text))
            send_text_message(event, vk)

            

if __name__ == "__main__":
    main()