from ..db.db_handler import db_handler
from ..utils.error_handler import ErrorHandler
from ..utils.messaging import MessagingService
from telegram import Update, Message
from telegram.ext import ContextTypes
import structlog
from typing import Optional

logger = structlog.get_logger()

async def add_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received add_quote command")
    message = update.message
    thread_id = message.message_thread_id if message else None
    quoted_msg = (
        update.effective_message.reply_to_message if update.effective_message else None
    )
    chat_id = update.effective_chat.id if update.effective_chat else None
    messaging = MessagingService(context.bot)
    error_handler = ErrorHandler()
    database = db_handler()
    if not quoted_msg:
        logger.warning("No message to quote", chat_id=chat_id, thread_id=thread_id)
        await messaging.send_message(chat_id, "Necesítase unha mensaxe para citar.", thread_id)
        return
    try:
        database.connect()
        cursor = database.execute("SELECT * FROM quotes WHERE quote = %s", (quoted_msg.text,))
        quotes = cursor.fetchall()
        log_text =  "Quote already exists"
        chat_text =  "Xa existe a cita."
        username = "Anonymous"
        if not quotes:      
            username = quoted_msg.from_user.username if quoted_msg.from_user else "Anonymous"
            database.execute("INSERT INTO quotes (quote, user) VALUES (%s, %s)", (quoted_msg.text, username))
            database.commit()
            log_text =  "Quote added"
            chat_text =  "Cita engadida."

        logger.info(log_text, quote=quoted_msg.text, user=username)
        await messaging.send_message(chat_id, chat_text, thread_id)

    except RuntimeError as err:
        await error_handler.handle_runtime_error(err, context, chat_id, thread_id)
    finally:
        database.close()