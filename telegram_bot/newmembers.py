from telegram import Update
from telegram.ext import ContextTypes
import random
import structlog

logger = structlog.get_logger()

welcome_messages = [
    "A wild @{username} appears!",
    "Ok, 200 @{username}, welcome",
    "Benvido @{username}",
    "Bienvenido a la grieta del invocador, @{username}",
    "You made it, @{username}!",
    "Speak friend and enter, @{username}",
]


async def new_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.new_chat_members:
        chat_id = update.message.chat_id
        new_member = (
            update.message.new_chat_members[0].username
            if update.message.new_chat_members[0].username
            else "Unknown"
        )

        logger.info(
            "New member detected",
            user_id=update.message.new_chat_members[0].id,
            username=new_member,
            chat_id=chat_id,
        )

        welcome_message = random.choice(welcome_messages).format(username=new_member)

        logger.debug(
            "Selected welcome message", message=welcome_message, username=new_member
        )

        await context.bot.send_message(chat_id, welcome_message, message_thread_id=1669)

        logger.info("Welcome message sent", chat_id=chat_id, message=welcome_message)
