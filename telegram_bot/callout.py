from telegram import Update
from telegram.ext import ContextTypes
import random
import structlog

logger = structlog.get_logger()

async def vigo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        "Vigo Callout command received",
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
            "Vigo Callout requested",
            user_id=update.message.from_user.id,
            username=update.message.from_user.username,
        )
      callout = ""
      with open("vigo.txt", "r", encoding="utf-8") as vigo_attendees:
            for line in vigo_attendees:
                callout += line + " "

      await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"{callout}",
            message_thread_id=thread_id,
        )
      logger.info(
            "Sent Vigo Callout message",
            chat_id=update.message.chat_id,
            thread_id=thread_id,
        )
      
    else:
        logger.info(
            "User Vigo Callout requested",
            user_id=update.message.from_user.id
            if update.message and update.message.from_user
            else None,
            username=update.message.from_user.username
            if update.message and update.message.from_user
            else None,
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id, # type: ignore
            text="Prohibido spamear",
            message_thread_id=thread_id,
        )

        logger.info(
            "Vigo Callout message not sent"
        )
    
    return