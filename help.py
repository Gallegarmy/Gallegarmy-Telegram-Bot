from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):  
    thread_id = update.message.message_thread_id
    print(thread_id)
    await context.bot.send_message(chat_id=update.message.chat_id, text="Commandos actualmente habilidatos en el bot:\n/start - Mensaje de bienvenida\n/cerveza - Información del próximo evento de admin cañas\n/pineapple - Un manjar tropical\n/help - Listado de comandos habilitados", message_thread_id=thread_id)
    return
