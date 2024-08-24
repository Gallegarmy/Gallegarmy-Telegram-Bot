from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    thread_id = update.message.message_thread_id
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="pong/", message_thread_id=thread_id
    )
