from telegram import Update
from telegram.ext import ContextTypes
import random
import structlog

logger = structlog.get_logger()


async def pinacolada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        "Pinacolada command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )

    if update.message is not None:
        thread_id = update.message.message_thread_id
    else:
        thread_id = None

    try:
        lines = open("pinacolada.txt").read().splitlines()
        logger.debug("Lines read from pinacolada.txt", line_count=len(lines))

        if update.effective_chat is not None:
            selected_line = random.choice(lines)
            logger.debug("Selected line to send", line=selected_line)

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=selected_line,
                message_thread_id=thread_id,
            )

            logger.info(
                "Pinacolada message sent",
                chat_id=update.effective_chat.id,
                message=selected_line,
            )
    except Exception as e:
        logger.error(
            "Error reading pinacolada.txt or sending message",
            error=str(e),
            user_id=update.effective_user.id if update.effective_user else None,
            chat_id=update.effective_chat.id if update.effective_chat else None,
        )
