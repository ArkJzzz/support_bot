#!usr/bin/python3

########################################################################
#    ToDo
# - добавить в if __name__ == "__main__": argparse
#
########################################################################

import os
import json
import google.auth
import argparse
import dialogflow_v2 as dialogflow
from dotenv import load_dotenv
from my_logger import get_logger

logger = get_logger('train_agent')

def create_intent(
    project_id, 
    display_name, 
    training_phrases_parts, 
    message_texts,
    ):
    """Create an intent of the given intent type."""
    
    intents_client = dialogflow.IntentsClient()

    parent = intents_client.project_agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message],
        )

    response = intents_client.create_intent(parent, intent)

    logger.info('Intent created: {}'.format(display_name))


def main():

    load_dotenv()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-credentials.json'
    credentials, project = google.auth.default()

    parser = argparse.ArgumentParser(
        description='Программа для обучения нейросети DialogFlow тренировочными фразами и ответами из файла .json'
        )
    parser.add_argument('-fn', '--filename', help='введите <имя_файла.json> с тренировочными фразами и ответами')
    args = parser.parse_args()

    try:
        with open(args.filename, "r") as questions_file:
            questions = json.load(questions_file)

        for display_name in questions:
            training_phrases_parts = questions[display_name]['questions']
            message_texts = [questions[display_name]['answer']]

            create_intent(
                project, 
                display_name, 
                training_phrases_parts, 
                message_texts,
                )

    except FileNotFoundError:
        logger.error('No such file or directory: {}'.format(args.filename))
    except google.api_core.exceptions.FailedPrecondition:
        logger.error('Intent with the display_name "{}" already exists'.format(display_name))


if __name__ == "__main__":
    main()