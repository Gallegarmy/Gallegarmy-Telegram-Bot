from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import threading


async def new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.new_chat_members:
                chat_id = update.message.chat_id
                user_id = update.message.new_chat_members[0].id
                await context.bot.send_message(chat_id, "Bienvenido á canle de Sysarmy Galicia, por favor envía unha mensaxe nos próximos 10 minutos para comprobar que non es un bot \n Bienvenido al canal de Sysarmy Galicia, por favor envía una mensaje en los próximos 10 minutos para comprobar que no eres un bot \n Welcome to the Sysarmy Galicia channel, please send a message within the followin 10 minutes to corroborate you are not a bot")

                # Start a timer to ban the user if they don't say hi in the next 10 minutes        
                threading.Timer(600, ban_user, args=[update, context, user_id]).start()

def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id):
    if not update.message:
        chat_id = update.message.chat_id
        update.chat_member.chat.ban_member(user_id=user_id)
        context.bot.send_message(chat_id, f'O usuario {user_id} non se presentou dentro dos 10 minutos')
