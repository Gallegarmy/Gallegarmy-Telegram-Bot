from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Text, Dict, Any

from telegram.ext import Application


class MessageSendingError(Exception):
    pass


@dataclass(frozen=True)
class Message:
    message: Text

    extra_args: Dict[str, Any]


class MessageSender(ABC):

    @abstractmethod
    def send(self, message: Message, **kwargs) -> None:
        pass


class TelegramMessageSender(MessageSender):

    def __init__(self, application: Application) -> None:
        self.application = application

    async def send(self, message: Message, **kwargs) -> None:
        try:
            await self.application.bot.send_message(
                text=message.message,
                chat_id=message.extra_args.get('chat_id'),
                message_thread_id=message.extra_args.get('thread_id'),
                **kwargs
            )
        except telegram.error.TelegramError as e:
            raise MessageSendingError('Error sending message to telegram') from e
