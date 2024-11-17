from typing import Callable, Dict, Text, Coroutine, Tuple, Optional, Any

from telegram import Update
from telegram.ext import Application, CallbackContext

from sysarmy_bot.core.message import User

TelegramHandler = Callable[[Update, CallbackContext], Coroutine[Any, Any, None]]
TelegramHandlers = Dict[Text, TelegramHandler]


class TelegramUpdateError(Exception):

    @classmethod
    def update_without_from_user(cls) -> 'TelegramUpdateError':
        return cls('Update received without user')


async def sender_from_message_update(update: Update) -> User:
    if update.message and update.message.from_user:
        return User(**{
            'id': update.message.from_user.id,
            'first_name': update.message.from_user.first_name,
            'last_name': update.message.from_user.last_name,
            'username': update.message.from_user.username,
            'language_iso2': update.message.from_user.language_code,
            'is_bot': update.message.from_user.is_bot,
        })

    raise TelegramUpdateError.update_without_from_user()


async def message_content_from_update_or_fail(update: Update) -> Tuple[int, Optional[Text], Optional[int]]:
    if update.message:
        return update.message.chat_id, update.message.text, update.message.message_thread_id

    raise TelegramUpdateError.update_without_from_user()


async def init_bot(bot: Application) -> None:
    await bot.initialize()
    await bot.start()
    await bot.updater.start_polling(allowed_updates=Update.ALL_TYPES)


async def shutdown_bot(bot: Application) -> None:
    if bot.updater.running:
        await bot.updater.stop()

    if bot.running:
        await bot.stop()
        await bot.shutdown()
