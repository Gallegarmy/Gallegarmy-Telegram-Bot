from telegram import Update
from telegram.ext import ContextTypes

async def add_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quoted_msg = update.effective_message.reply_to_message
    print(quoted_msg.text)
    print(quoted_msg.from_user.username)
