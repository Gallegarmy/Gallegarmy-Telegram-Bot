from typing import Callable, Any, Coroutine

from telegram import Update
from telegram.ext import CallbackContext

from sysarmy_bot.core.help.help_message_handler import HelpMessage
from sysarmy_bot.shared.message_bus import MessageBus
from sysarmy_bot.shared.telegram_utils import (
    sender_from_message_update,
    message_content_from_update_or_fail
)


def new_wrapped_help_message_handler(
        message_bus: MessageBus
) -> Callable[[Update, CallbackContext], Coroutine[Any, Any, None]]:
    async def handler(update: Update, context: CallbackContext):
        sender = await sender_from_message_update(update)
        chat_id, text, thread_id = await message_content_from_update_or_fail(update)
        help_message = HelpMessage(
            user_id=sender.id,
            chat_id=chat_id,
            message=text,
            thread_id=thread_id,
            sender=sender
        )

        await message_bus.handle(help_message)

    return handler
