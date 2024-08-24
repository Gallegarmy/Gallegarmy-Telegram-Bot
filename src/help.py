from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    thread_id = update.message.message_thread_id
    print(thread_id)
    admins = [line.strip() for line in open("admins.txt")]
    if str(update.message.from_user.username) in admins:
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

        await context.bot.send_message(
            chat_id=update.message.chat_id, text=f"{help}", message_thread_id=thread_id
        )
        return
