#!usr/bin/python3

########################################################################
#    ToDo
# - добавить в if __name__ == "__main__": argparse
#
#
#
########################################################################

import os
import json
import google.auth
from dotenv import load_dotenv


def create_intent(
    project_id, 
    display_name, 
    training_phrases_parts, 
    message_texts,
    ):
    """Create an intent of the given intent type."""
    import dialogflow_v2 as dialogflow
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

    print('Intent created: {}'.format(response))


def main():

    load_dotenv()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'df_key.json'
    credentials, project = google.auth.default()

    with open("questions.json", "r") as questions_file:
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



if __name__ == "__main__":
    main()
