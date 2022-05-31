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
    return response.query_result.fulfillment_text

