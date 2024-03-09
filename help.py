from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Commandos actualmente habilidatos en el bot:\n/start - Mensaje de bienvenida\n/cañas - Información del próximo evento de admin cañas\n/help - Listado de comandos habilitados")

