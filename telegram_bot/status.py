from telegram import Update
from telegram.ext import ContextTypes


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is not None:
        thread_id = update.message.message_thread_id
    else:
        thread_id = None  # or handle the case when there is no message
    if update.effective_chat is not None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="pong/", message_thread_id=thread_id
        )
