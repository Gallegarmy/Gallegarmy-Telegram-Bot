from telegram import Update, Chat
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import threading


async def new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.new_chat_members:
                chat_id = update.message.chat_id
                await context.bot.send_message(chat_id, f"A wild @{update.message.new_chat_members[0].username} appears", message_thread_id=1669)
      
