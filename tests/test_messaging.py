import asyncio
from unittest.mock import AsyncMock, MagicMock

from telegram_bot.utils.messaging import MessagingService


def run(coro):
    return asyncio.run(coro)


def _bot_mock():
    bot = MagicMock()
    bot.send_message = AsyncMock()
    return bot


def test_send_message_calls_bot_with_correct_args():
    bot = _bot_mock()
    run(MessagingService(bot).send_message(chat_id=42, text="hello"))
    bot.send_message.assert_called_once_with(
        chat_id=42, text="hello", message_thread_id=None
    )


def test_send_message_passes_thread_id():
    bot = _bot_mock()
    run(MessagingService(bot).send_message(chat_id=42, text="hi", thread_id=7))
    bot.send_message.assert_called_once_with(
        chat_id=42, text="hi", message_thread_id=7
    )


def test_send_message_skips_when_chat_id_is_none():
    bot = _bot_mock()
    run(MessagingService(bot).send_message(chat_id=None, text="lost message"))
    bot.send_message.assert_not_called()
