from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type, TypeVar, Optional

from sysarmy_bot.shared.logger import Logger

Result = TypeVar('Result')


@dataclass(frozen=True)
class Dto(ABC):

    @staticmethod
    @abstractmethod
    def id() -> str:
        pass


class InvalidDto(Exception):

    def __init__(self, message: str):
        self.message = message


class MessageHandler(ABC):

    @abstractmethod
    def handle(self, message: Dto) -> Optional[Result]:
        pass


class MessageBus(ABC):
    @abstractmethod
    async def register_message_handler(self, message: Type[Dto], handler: MessageHandler) -> None:
        pass

    @abstractmethod
    async def handle(self, message: Dto) -> Optional[Result]:
        pass


class AwaitableMessageBus(MessageBus):

    def __init__(self, logger: Logger):
        self.logger = logger
        self.handlers: Dict[Text, MessageHandler] = dict()

    async def register_message_handler(self, message: Type[Dto], handler: MessageHandler) -> None:
        message_name = message.id()

        if message_name in self.handlers:
            raise InvalidDto('Command <%s> already registered' % message_name)

        self.handlers[message_name] = handler

    async def handle(self, message: Dto) -> Optional[Result]:
        message_name = message.id()
        if message_name in self.handlers:
            handler = self.handlers[message_name]
            self.logger.info(f'Handling message <{handler.__class__}:{message_name}>')

            return await handler.handle(message)

        raise InvalidDto('Command <%s> not registered' % message_name)
