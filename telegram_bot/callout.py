from telegram import Update
from telegram.ext import ContextTypes
from telegram_bot.utils.callout_function import construct_callout
import random
import structlog


async def vigo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if update.message is not None:
        thread_id = update.message.message_thread_id
    else:
        thread_id = None

    admins = [line.strip() for line in open("admins.txt")]

    if (
        update.message is not None
        and update.message.from_user is not None
        and str(update.message.from_user.username) in admins
    ):

      await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"{construct_callout("Vigo")}",
            message_thread_id=thread_id,
        )      
      
    else:

        await context.bot.send_message(
            chat_id=update.effective_chat.id, # type: ignore
            text="Prohibido spamear",
            message_thread_id=thread_id,
        )

    
    return 


async def coruna(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is not None:
        thread_id = update.message.message_thread_id
    else:
        thread_id = None

    admins = [line.strip() for line in open("admins.txt")]

    if (
        update.message is not None
        and update.message.from_user is not None
        and str(update.message.from_user.username) in admins
    ):

      await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"{construct_callout("Coruña")}",
            message_thread_id=thread_id,
        )
      
    else:

        await context.bot.send_message(
            chat_id=update.effective_chat.id, # type: ignore
            text="Prohibido spamear",
            message_thread_id=thread_id,
        )

    return