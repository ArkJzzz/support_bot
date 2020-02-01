#!usr/bin/python3

# Copyright 2017 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""DialogFlow API Detect Intent Python sample with text inputs.

Examples:
  python detect_intent_texts.py -h
  python detect_intent_texts.py --project-id PROJECT_ID \
  --session-id SESSION_ID \
  "hello" "book a meeting room" "Mountain View"
  python detect_intent_texts.py --project-id PROJECT_ID \
  --session-id SESSION_ID \
  "tomorrow" "10 AM" "2 hours" "10 people" "A" "yes"
"""


import argparse
import uuid
import dialogflow_v2 as dialogflow
from my_logger import get_logger


logger = get_logger('detect_intent')

def detect_intent_text(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, 
        query_input=query_input,
        )

    logger.info('Query text: {}'.format(response.query_result.query_text))
    logger.info('Action: {}'.format(response.query_result.action))
    logger.info('Detected intent: {} (confidence: {})'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    logger.info('Fulfillment text: {}\n'.format(
         response.query_result.fulfillment_text))

    return response.query_result


if __name__ == '__main__':
    print('this is a module')

