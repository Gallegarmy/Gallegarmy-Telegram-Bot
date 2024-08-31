from telegram import Update, Message
from telegram.ext import ContextTypes
import os
import mysql.connector
from typing import Optional
import structlog

logger = structlog.get_logger()


async def add_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received add_quote command")
    database = None

    message = update.message
    thread_id: Optional[int] = message.message_thread_id if message else None
    quoted_msg: Optional[Message] = (
        update.effective_message.reply_to_message if update.effective_message else None
    )
    chat_id: Optional[int] = update.effective_chat.id if update.effective_chat else None

    if quoted_msg is None:
        logger.warning("No message to quote", chat_id=chat_id, thread_id=thread_id)
        if chat_id is not None:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Necesítase unha mensaxe para citar.",
                message_thread_id=thread_id,
            )
        return

    try:
        database = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST"),
            user=os.environ.get("MYSQL_USER"),
            password=os.environ.get("MYSQL_PASSWORD"),
            database=os.environ.get("MYSQL_DATABASE"),
        )
        cursor = database.cursor()
        SQLCheckQuote = "SELECT * FROM quotes WHERE quote = %s"
        cursor.execute(SQLCheckQuote, (quoted_msg.text,))
        quotes = cursor.fetchall()

        if len(quotes) == 0:
            username = (
                quoted_msg.from_user.username if quoted_msg.from_user else "Anonymous"
            )
            SQLAddQuote = "INSERT INTO quotes (quote, user) VALUES (%s,%s)"
            cursor.execute(SQLAddQuote, (quoted_msg.text, username))
            logger.info("Quote added", quote=quoted_msg.text, user=username)

            if chat_id is not None:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Cita agregada.",
                    message_thread_id=thread_id,
                )
            database.commit()
        else:
            logger.info("Quote already exists", quote=quoted_msg.text)
            if chat_id is not None:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Xa existe a cita.",
                    message_thread_id=thread_id,
                )
    except mysql.connector.Error as err:
        logger.error("Database error", error=str(err))
    finally:
        if database:
            database.close()
            logger.debug("Database connection closed")


async def random_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received random_quote command")

    message = update.message
    thread_id: Optional[int] = message.message_thread_id if message else None
    chat_id: Optional[int] = update.effective_chat.id if update.effective_chat else None

    database = None
    try:
        database = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST"),
            user=os.environ.get("MYSQL_USER"),
            password=os.environ.get("MYSQL_PASSWORD"),
            database=os.environ.get("MYSQL_DATABASE"),
        )
        cursor = database.cursor()

        if context.args is not None and len(context.args) == 1:
            user = context.args[0]
            if user[0] == "@":
                user = user[1:]
            logger.debug("Searching quotes for user", user=user)

            SQLSearchUserQuote = (
                "SELECT quote FROM quotes WHERE user = %s ORDER BY RAND () LIMIT 3"
            )
            cursor.execute(SQLSearchUserQuote, (user,))
            quotes = cursor.fetchall()

            if quotes:
                user_quotes = f"Quotes ao azar de {user}:"
                for quote_tuple in quotes:
                    (quote,) = quote_tuple
                    user_quotes += f"\n{quote}"
                logger.info("User quotes found", user=user, quotes=user_quotes)

                if chat_id is not None:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=user_quotes,
                        message_thread_id=thread_id,
                    )
            else:
                logger.info("No quotes found for user", user=user)
                if chat_id is not None:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text="Non se atoparon quotes dese usuario",
                        message_thread_id=thread_id,
                    )
        elif context.args is not None and len(context.args) < 1:
            logger.debug("Searching for random quote")
            SQLSearchRandomQuote = (
                "SELECT quote, user FROM quotes ORDER BY RAND () LIMIT 1"
            )
            cursor.execute(SQLSearchRandomQuote)
            result = cursor.fetchone()
            if result:
                quote, user = result
                random_quote = (
                    f"Quote ao azar de Sysarmy Galicia:\nAutor {user}: {quote}"
                )
                logger.info("Random quote found", user=user, quote=quote)

                if chat_id is not None:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=random_quote,
                        message_thread_id=thread_id,
                    )
            else:
                logger.info("No quotes found")
                if chat_id is not None:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text="Non se atoparon citas.",
                        message_thread_id=thread_id,
                    )
        else:
            logger.warning("Too many arguments provided", args=context.args)
            if chat_id is not None:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Pasáronse máis argumentos dos permitidos",
                    message_thread_id=thread_id,
                )
    except mysql.connector.Error as err:
        logger.error("Database error", error=str(err))
    finally:
        if database:
            database.close()
            logger.debug("Database connection closed")
