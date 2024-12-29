import os
from ..db.db_handler import DbHandler
from ..db.karma_facade import update_karma
from ..utils.error_handler import ErrorHandler
from ..utils.messaging import MessagingService
from telegram import Update
from telegram.ext import ContextTypes
from collections import defaultdict
import datetime
import structlog
import logging

karma_limit = defaultdict(lambda: 5)
last_cleared_date = None
level = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_LEVEL = getattr(logging, level)
structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(LOG_LEVEL))
logger = structlog.get_logger()
ADD = 1
REMOVE = -1

async def kup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await handle_karma(update, context, "add")

async def kdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await handle_karma(update, context, "remove")


async def handle_karma(update: Update, context: ContextTypes.DEFAULT_TYPE, operation: str):
    """Handles karma commands: add, remove, show, and list."""
    global karma_limit, last_cleared_date
    now = datetime.datetime.now()
    error_handler = ErrorHandler()

    if last_cleared_date is None or now.date() > last_cleared_date:
        karma_limit.clear()
        last_cleared_date = now.date()
    thread_id = update.message.message_thread_id if update.message else None
    chat_id = update.effective_chat.id if update.effective_chat else None
    messaging = MessagingService(context.bot)
    database = DbHandler()
    user = update.message.from_user.username
    target = context.args[0] if context.args else None

    if operation == "add" or operation == "remove":
        if not target or user == target:
            await messaging.send_message(chat_id, text="Invalid target for karma operation.", thread_id=thread_id)
            return

        if karma_limit[user] == 0:
            await messaging.send_message(chat_id, text="Karma limit reached for today.", thread_id=thread_id)
            return

        karma_op = ADD if operation == "add" else REMOVE

        username = target.lower().removeprefix('@')
        new_karma = update_karma(username, karma_op, target.startswith('@'))
        karma_limit[user] -= 1
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"{target} karma updated: {new_karma}")

    elif operation == "list":
        karma_summary = database.execute()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=karma_summary)

    elif operation == "show":
        target_karma = get_or_create_user_karma(target)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"Karma for {target}: {target_karma}")
