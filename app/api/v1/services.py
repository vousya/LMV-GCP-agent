from google.cloud import dialogflowcx_v3

from dotenv import load_dotenv
from pathlib import Path
import os

import asyncio

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

env_path = Path(__file__).resolve().parents[2] / "core" / ".env"
load_dotenv(dotenv_path=env_path)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
print("\n\n\ntelegram token:", TELEGRAM_TOKEN)
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

PROJECT_ID = "chat-bot-453509"
AGENT_ID = "8dbd0bd8-b187-4738-a3f3-177ad9acb52c"
LOCATION = "global"


class AgentService:
    def __init__(self):
        self.app = None

    async def start_bot(self):
        print("Starting bot connection...")
        self.app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_message))
        await self.app.initialize()
        await self.app.start()  # start polling (non-blocking)
        print("Bot started.")

    async def end_bot(self):
        print("Stopping bot...")
        if self.app:
            await self.app.stop()
            await self.app.shutdown()
        print("Bot stopped.")

    @staticmethod
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        chat_id = update.message.chat.id
        session_id = str(chat_id)
        print("message: ", update.message)

        try:
            client = dialogflowcx_v3.SessionsClient()
            session_path = f"projects/{PROJECT_ID}/locations/{LOCATION}/agents/{AGENT_ID}/sessions/{session_id}"
            text_input = dialogflowcx_v3.TextInput(text=text)
            query_input = dialogflowcx_v3.QueryInput(text=text_input, language_code="uk")
            request = dialogflowcx_v3.DetectIntentRequest(session=session_path, query_input=query_input)

            response = await asyncio.to_thread(client.detect_intent, request=request)
            bot_response = response.query_result.response_messages[0].text.text[0]

            print("Response in bot: ", bot_response)
            await context.bot.send_message(chat_id=chat_id, text=bot_response)

        except Exception as e:
            await context.bot.send_message(chat_id=chat_id, text=f"Error: {e}")


agent_service = AgentService()
