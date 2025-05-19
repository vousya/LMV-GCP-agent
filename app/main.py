from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.v1.services import agent_service


from api.v1 import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await agent_service.start_bot()
    print("Telegram bot connected")
    yield
    await agent_service.end_bot()
    print("Telegram bot disconnected")

app = FastAPI(lifespan=lifespan)

app.include_router(router)