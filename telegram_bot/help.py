from telegram import Update
from telegram.ext import ContextTypes


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is not None:
        thread_id = update.message.message_thread_id
    else:
        thread_id = None

    admins = [line.strip() for line in open("admins.txt")]

    if (
        update.message is not None
        and update.message.from_user is not None
        and str(update.message.from_user.username) in admins
    ):
        help = ""
        with open("helpadmin.txt", "r", encoding="utf-8") as help_file:
            for line in help_file:
                help = help + line
                help = help + "\n"
        await context.bot.send_message(
            chat_id=update.message.chat_id, text=f"{help}", message_thread_id=thread_id
        )
        return
    else:
        help = ""
        with open("help.txt", "r", encoding="utf-8") as help_file:
            for line in help_file:
                help = help + line
                help = help + "\n"
        if update.message is not None:
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text=f"{help}",
                message_thread_id=thread_id,
            )
        return
