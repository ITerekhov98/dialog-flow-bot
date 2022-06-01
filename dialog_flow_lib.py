import argparse
import json

from google.cloud import dialogflow
from environs import Env

env = Env()


def fetch_intent_response(session_id, text, language_code='ru'):
    project_id = env.str('GOOGLE_PROJECT_ID')
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response


def add_intents(filepath_to_questions: str, google_project_id):
    with open(filepath_to_questions, 'r') as f:
        serialized_questions = json.load(f)
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(google_project_id)
    for display_name in serialized_questions.keys():
        training_phrases = []
        for training_phrases_part in serialized_questions[display_name]['questions']:
            part = dialogflow.Intent.TrainingPhrase.Part(
                text=training_phrases_part
            )
            training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
            training_phrases.append(training_phrase)

        text = dialogflow.Intent.Message.Text(
            text=[serialized_questions[display_name]['answer']]
        )
        message = dialogflow.Intent.Message(text=text)
        intent = dialogflow.Intent(
            display_name=display_name,
            training_phrases=training_phrases,
            messages=[message]
        )
        response = intents_client.create_intent(
            request={"parent": parent, "intent": intent}
        )
        print("Intent created: {}".format(response))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_learn_file")
    args = parser.parse_args()
    env.read_env()
    google_project_id = env.str('GOOGLE_PROJECT_ID')
    print(google_project_id)
    add_intents(args.path_to_learn_file, google_project_id)

if __name__ == '__main__':
    main()

