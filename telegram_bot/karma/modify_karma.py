import os
import mysql.connector
from ..db.db_handler import db_handler
from ..utils.error_handler import ErrorHandler
from ..utils.messaging import MessagingService
from telegram import Update
from telegram.ext import ContextTypes
from collections import defaultdict
import datetime
import structlog
import functools

from telegram_bot.utils.tgram_utils import get_user

karmaLimit = defaultdict(int)
last_cleared_date = None
structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(LOG_LEVEL))
logger = structlog.get_logger()


async def modify_karma(update: Update, context: ContextTypes.DEFAULT_TYPE, operation: str):
    global karmaLimit, last_cleared_date
    now = datetime.datetime.now()
    messaging = MessagingService(context.bot)

    if last_cleared_date is None or now.date() > last_cleared_date:
        karmaLimit.clear()
        last_cleared_date = now.date()
        logger.debug("Karma limits cleared", date=last_cleared_date)

    if not update.message or not update.message.from_user or not update.effective_chat:
        logger.warning("No message context available for karma operation")
        return None

    executing_username = update.message.from_user.username
    thread_id = update.message.message_thread_id
    chat_id = update.effective_chat.id
    target_username = ''

    if update.message.reply_to_message:
        detected_user = update.message.reply_to_message.from_user
        if detected_user:
            target_username = detected_user.username or detected_user.first_name
    elif context.args:
        target_username = str(context.args[0])

    if not target_username:
        await messaging.send_message(chat_id, "Necesito un usuario para asignarlle/quitarlle karma", thread_id)
        logger.warning(
            "Karma command received without arguments",
            user_id=update.effective_user.id if update.effective_user else None,
        )
        return None

    if target_username.lower() == executing_username.lower():
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Non sexas tan egocéntrico tío",
            message_thread_id=thread_id,
        )
        logger.warning(
            "User tried to give/remove karma to themselves",
            user=executing_username,
        )
        return None

    if executing_username not in karmaLimit:
        karmaLimit[executing_username] = 5

    if karmaLimit[executing_username] == 0:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Xa non podes asignar/quitar máis karma hoxe",
            message_thread_id=thread_id,
        )
        logger.info("Karma limit reached", user=executing_username)
        return None

    database = mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST"),
        user=os.environ.get("MYSQL_USER"),
        password=os.environ.get("MYSQL_PASSWORD"),
        database=os.environ.get("MYSQL_DATABASE"),
    )
    cursor = database.cursor()

    # Check if user exists in the karma database and update or create accordingly
    SQLUsers = "SELECT * FROM karma WHERE word = %s"
    cursor.execute(SQLUsers, (target_username.lower(),))
    usuarios = cursor.fetchall()

    if not usuarios:
        # User does not exist in the karma table; insert them with initial karma
        karma_value = 1 if operation == "add" else -1
        SQLCreateuser = "INSERT INTO karma (word, karma, is_user) VALUES (%s, %s, %s)"
        cursor.execute(SQLCreateuser, (target_username.lower().removeprefix('@'), karma_value, target_username[0] == '@'))
        logger.info("New user created in karma database", user=target_username)
    else:
        # Update existing user's karma
        SQLUpdateKarma = "UPDATE karma SET karma = karma + %s WHERE word = %s"
        karma_change = 1 if operation == "add" else -1
        cursor.execute(SQLUpdateKarma, (karma_change, target_username.lower().removeprefix('@')))
        logger.info("Karma updated for user", user=target_username)

    # Commit and close database connection
    database.commit()
    database.close()

    # Deduct from user’s karma limit
    karmaLimit[executing_username] -= 1

    # Return the target username and thread ID for follow-up messaging
    return [target_username, thread_id]