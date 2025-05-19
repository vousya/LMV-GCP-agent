from google.cloud import dialogflowcx_v3

import asyncio

from dotenv import load_dotenv
from pathlib import Path
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

env_path = Path(__file__).resolve().parents[1] / "app" / "core" / ".env"
load_dotenv(dotenv_path=env_path)  # Loads GOOGLE_APPLICATION_CREDENTIALS

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

PROJECT_ID = "chat-bot-453509"
AGENT_ID = "8dbd0bd8-b187-4738-a3f3-177ad9acb52c"
LOCATION = "global"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat.id
    session_id = str(chat_id)
    print("message: ", update.message.text)

    try:
        client = dialogflowcx_v3.SessionsClient()
        session_path = f"projects/{PROJECT_ID}/locations/{LOCATION}/agents/{AGENT_ID}/sessions/{session_id}"

        text_input = dialogflowcx_v3.TextInput(text=text)
        query_input = dialogflowcx_v3.QueryInput(text=text_input, language_code="uk")

        request = dialogflowcx_v3.DetectIntentRequest(session=session_path, query_input=query_input)
        response = await asyncio.to_thread(client.detect_intent, request=request)

        print(response.query_result.response_messages)
        bot_response = response.query_result.response_messages[0].text.text[0]

        print("Response in bot: ", bot_response)
        await context.bot.send_message(chat_id=chat_id, text=bot_response)

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"Error: {e}")


app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

app.run_polling()
