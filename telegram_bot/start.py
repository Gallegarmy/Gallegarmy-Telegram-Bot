from telegram import Update
from telegram.ext import ContextTypes
import structlog

logger = structlog.get_logger()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        "Start command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )

    if update.message is not None:
        thread_id = update.message.message_thread_id
    else:
        thread_id = None

    if update.effective_chat is not None:
        welcome_message = (
            "Boas, son o bot de gallegarmy, para axudar á comunidade no que necesite!"
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=welcome_message,
            message_thread_id=thread_id,
        )

        logger.info(
            "Start message sent",
            chat_id=update.effective_chat.id,
            message=welcome_message,
        )
