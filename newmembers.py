from telegram import Update, Chat
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import threading


async def new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.new_chat_members:
                chat_id = update.message.chat_id
                await context.bot.send_message(chat_id, "Bienvenido á canle de Sysarmy Galicia, esperamos que o pases moi ben nesta comunida! \n\n Bienvenido al canal de Sysarmy Galicia, esperamos que lo pases muy bien en esta comunida!\n\n Welcome to the Sysarmy Galicia channel, we hope you have a great time within this community!", message_thread_id=1669)
      
