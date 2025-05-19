from fastapi import APIRouter

from .services import agent_service
from core.schemas import Message


router = APIRouter(tags=["Agent"])

@router.post(
    "/dialogflow"
)
async def get_answer(
        message : Message
):
    #response = await agent_service.get_answer(text=message.text, session_id=message.session_id)

    #return {"response": response}
    pass
