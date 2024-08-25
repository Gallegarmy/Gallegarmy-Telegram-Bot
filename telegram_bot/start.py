from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is not None:
        thread_id = update.message.message_thread_id
    else:
        thread_id = None
    if update.effective_chat is not None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Boas, son o bot de gallegarmy, para axudar á comunidade no que necesite!",
            message_thread_id=thread_id,
        )
