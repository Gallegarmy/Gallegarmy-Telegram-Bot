from telegram import Update, Message
from telegram.ext import ContextTypes
import os
import mysql.connector
from typing import Optional


async def add_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    thread_id: Optional[int] = message.message_thread_id if message else None
    quoted_msg: Optional[Message] = (
        update.effective_message.reply_to_message if update.effective_message else None
    )
    chat_id: Optional[int] = update.effective_chat.id if update.effective_chat else None

    if quoted_msg is None:
        if chat_id is not None:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Necesítase unha mensaxe para citar.",
                message_thread_id=thread_id,
            )
        return

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
        username = quoted_msg.from_user.username if quoted_msg.from_user else None
        SQLAddQuote = "INSERT INTO quotes (quote, user) VALUES (%s,%s)"
        cursor.execute(SQLAddQuote, (quoted_msg.text, username or "Anonymous"))

        if chat_id is not None:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Cita agregada.",
                message_thread_id=thread_id,
            )
        database.commit()
    else:
        if chat_id is not None:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Xa existe a cita.",
                message_thread_id=thread_id,
            )
    database.close()


async def random_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    thread_id: Optional[int] = message.message_thread_id if message else None
    chat_id: Optional[int] = update.effective_chat.id if update.effective_chat else None

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
        SQLSearchUserQuote = (
            "SELECT quote FROM quotes WHERE user = %s ORDER BY RAND () LIMIT 3"
        )
        cursor.execute(SQLSearchUserQuote, (user,))
        quotes = cursor.fetchall()
        if quotes:
            user_quotes = f"Quotes ao azar de {user}:"
            for quote_tuple in quotes:
                quote = quote_tuple
                user_quotes += f"\n{quote}"
            if chat_id is not None:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=user_quotes,
                    message_thread_id=thread_id,
                )
        else:
            if chat_id is not None:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Non se atoparon quotes dese usuario",
                    message_thread_id=thread_id,
                )
    elif context.args is not None and len(context.args) < 1:
        SQLSearchRandomQuote = "SELECT quote, user FROM quotes ORDER BY RAND () LIMIT 1"
        cursor.execute(SQLSearchRandomQuote)
        result = cursor.fetchone()
        if result:
            quote, user = result
            random_quote = f"Quote ao azar de Sysarmy Galicia:\nAutor {user}: {quote}"
            if chat_id is not None:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=random_quote,
                    message_thread_id=thread_id,
                )
        else:
            if chat_id is not None:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Non se atoparon citas.",
                    message_thread_id=thread_id,
                )
    else:
        if chat_id is not None:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Pasáronse máis argumentos dos permitidos",
                message_thread_id=thread_id,
            )
    database.close()
