from telegram import Update
from telegram.ext import ContextTypes
import structlog

logger = structlog.get_logger()


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        "Help command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )

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
        logger.info(
            "Admin help requested",
            user_id=update.message.from_user.id,
            username=update.message.from_user.username,
        )

        help_message = ""
        with open("helpadmin.txt", "r", encoding="utf-8") as help_file:
            for line in help_file:
                help_message += line + "\n"

        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"{help_message}",
            message_thread_id=thread_id,
        )
        logger.info(
            "Sent admin help message",
            chat_id=update.message.chat_id,
            thread_id=thread_id,
        )
        return
    else:
        logger.info(
            "User help requested",
            user_id=update.message.from_user.id
            if update.message and update.message.from_user
            else None,
            username=update.message.from_user.username
            if update.message and update.message.from_user
            else None,
        )

        help_message = ""
        with open("help.txt", "r", encoding="utf-8") as help_file:
            for line in help_file:
                help_message += line + "\n"

        if update.message is not None:
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text=f"{help_message}",
                message_thread_id=thread_id,
            )
            logger.info(
                "Sent user help message",
                chat_id=update.message.chat_id,
                thread_id=thread_id,
            )
        return
