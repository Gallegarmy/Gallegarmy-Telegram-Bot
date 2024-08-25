from telegram import Update
from telegram.ext import ContextTypes
import random


async def pinacolada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is not None:
        thread_id = update.message.message_thread_id
    else:
        thread_id = None
    lines = open("pinacolada.txt").read().splitlines()
    if update.effective_chat is not None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=random.choice(lines),
            message_thread_id=thread_id,
        )
