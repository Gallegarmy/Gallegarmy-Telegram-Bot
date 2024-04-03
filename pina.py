from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import random

async def pinacolada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lines = open("pinacolada.txt").read().splitlines()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(lines))