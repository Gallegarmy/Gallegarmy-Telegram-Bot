from telegram import Update, Chat
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import threading, random


welcome_messages = [
    "A wild @{username} appears!",
    "Ok, 202 @{username}, welcome",
    "Benvido @{username}",
    "Bienvenido a la grieta del invocador, @{username}",
    "You made it, @{username}!",
    "Speak friend and enter, @{username}"
]

async def new_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.message.new_chat_members:
                chat_id = update.message.chat_id
                welcome_message = random.choice(welcome_messages).format(username=update.message.new_chat_members[0].username)
                await context.bot.send_message(chat_id, welcome_message, message_thread_id=1669)
      
