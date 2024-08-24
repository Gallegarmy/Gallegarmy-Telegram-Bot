from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    thread_id = update.message.message_thread_id
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Boas, son o bot de gallegarmy, para axudar á comunidade no que necesite!",
        message_thread_id=thread_id,
    )
