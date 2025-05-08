from fastapi import HTTPException
from google.cloud import dialogflowcx_v3

PROJECT_ID = "chat-bot-453509"
AGENT_ID = "volleyball-chatbot_1744129366076"
LOCATION = "global"

class AgentService:

    @classmethod
    async def get_answer(cls, text, session_id):
        try:
            client = dialogflowcx_v3.SessionsClient()
            session_path = f"projects/{PROJECT_ID}/locations/{LOCATION}/agents/{AGENT_ID}/sessions/{session_id}"
            text_input = dialogflowcx_v3.TextInput(text=text)
            query_input = dialogflowcx_v3.QueryInput(text=text_input, language_code="uk")
            request = dialogflowcx_v3.DetectIntentRequest(session=session_path, query_input=query_input)
            response = client.detect_intent(request=request)
            return response.query_result.response_messages[0].text.text[0]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Dialogflow error: {str(e)}")


agent_service = AgentService
