import os
import datetime
from collections import defaultdict
from telegram import Update
from telegram.ext import ContextTypes
from ..db.db_handler import db_handler
from ..utils.messaging import MessagingService
from ..utils.error_handler import ErrorHandler
import structlog

logger = structlog.get_logger()

karma_limit = defaultdict(lambda: 5)
last_cleared_date = None

async def handle_karma(operation: str):
    """Handles karma commands: add, remove, show, and list."""
    async def command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        global karma_limit, last_cleared_date
        now = datetime.datetime.now()
        error_handler = ErrorHandler()
        
        if last_cleared_date is None or now.date() > last_cleared_date:
            karma_limit.clear()
            last_cleared_date = now.date()
        thread_id = update.message.message_thread_id if update.message else None
        chat_id = update.effective_chat.id if update.effective_chat else None
        messaging = MessagingService(context.bot)
        database = db_handler()
        try:
            database.connect()
            user = update.message.from_user.username            
            target = context.args[0] if context.args else None

            if operation == "add" or operation == "remove":
                if not target or user == target:
                    await messaging.send_message(chat_id, text="Invalid target for karma operation.", thread_id)
                    return
                
                if karma_limit[user] == 0:
                    await messaging.send_message(chat_id, text="Karma limit reached for today.", thread_id)
                    return
                
                karma_change = 1 if operation == "add" else -1
                new_karma = update_karma(target, karma_change)
                karma_limit[user] -= 1
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{target} karma updated: {new_karma}")
            
            elif operation == "list":
                karma_summary = database.execute()
                await context.bot.send_message(chat_id=update.effective_chat.id, text=karma_summary)
            
            elif operation == "show":
                target_karma = get_or_create_user_karma(target)
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Karma for {target}: {target_karma}")
        except RuntimeError as err:
            await error_handler.handle_runtime_error(err, context, chat_id, thread_id)
        finally:
            database.close()

    return command