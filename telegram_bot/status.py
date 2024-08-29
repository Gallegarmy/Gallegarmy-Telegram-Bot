from telegram import Update
from telegram.ext import ContextTypes
import structlog

logger = structlog.get_logger()


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        "ping command received",
        user_id=update.effective_user.id if update.effective_user is not None else None,
        chat_id=update.effective_chat.id if update.effective_chat is not None else None,
    )

    if update.message is not None:
        thread_id = update.message.message_thread_id
        logger.info(
            "Message received",
            message_id=update.message.message_id,
            thread_id=thread_id,
        )
    else:
        thread_id = None
        logger.warning(
            "No message found in update",
            user_id=update.effective_user.id
            if update.effective_user is not None
            else None,
            chat_id=update.effective_chat.id
            if update.effective_chat is not None
            else None,
        )

    if update.effective_chat is not None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="pong/", message_thread_id=thread_id
        )
        logger.info(
            "pong message sent", chat_id=update.effective_chat.id, thread_id=thread_id
        )
    else:
        logger.error(
            "No effective chat found",
            user_id=update.effective_user.id
            if update.effective_user is not None
            else None,
        )
