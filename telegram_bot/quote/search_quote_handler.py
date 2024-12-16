from ..db.db_handler import db_handler
from ..utils.error_handler import ErrorHandler
from ..utils.messaging import MessagingService
from telegram import Update, Message
from telegram.ext import ContextTypes
import structlog
from typing import Optional

logger = structlog.get_logger()

async def search_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received random_quote command")
    message = update.message
    thread_id = message.message_thread_id if message else None
    chat_id = update.effective_chat.id if update.effective_chat else None
    messaging = MessagingService(context.bot)
    error_handler = ErrorHandler()
    database = db_handler()
    try:
        database.connect()
        if context.args and len(context.args) == 1:
            user = context.args[0].lstrip("@")
            logger.debug("Searching quotes for user", user=user)
            cursor = database.execute("SELECT quote FROM quotes WHERE user = %s ORDER BY RAND() LIMIT 3", (user,))
            quotes = cursor.fetchall()
            if quotes:
                user_quotes = f"Quotes ao azar de {user}:" + "".join(f"\n{quote}" for quote in quotes)
                logger.info("User quotes found", user=user, quotes=user_quotes)
                await messaging.send_message(chat_id, f"Quotes ao azar de {user}:" + "".join(f"\n{quote}" for quote in quotes), thread_id)
            else:
                logger.info("No quotes found for user", user=user)
                await messaging.send_message(chat_id, "Non se atoparon quotes dese usuario", thread_id)

        else:
            cursor = database.execute("SELECT quote, user FROM quotes ORDER BY RAND() LIMIT 1")
            result = cursor.fetchone()
            if result:
                logger.info("Random quote found", user=result['user'], quote=result['quote'])
                await messaging.send_message(chat_id, f"Quote ao azar de Sysarmy Galicia:\nAutor {result['user']}: {result['quote']}", thread_id)
            else:
                logger.info("No quotes found")
                await messaging.send_message(chat_id, "Non se atoparon citas.", thread_id)
    except RuntimeError as err:
        await error_handler.handle_runtime_error(err, context, chat_id, thread_id)
    finally:
        database.close()