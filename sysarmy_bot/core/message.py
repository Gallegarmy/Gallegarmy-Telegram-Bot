from dataclasses import dataclass, field
from typing import Text, Optional

from sysarmy_bot.shared.message_bus import Dto


@dataclass(frozen=True)
class User:
    id: int
    first_name: Text
    last_name: Text
    username: Text
    language_iso2: Optional[Text] = field(default=None)
    is_bot: bool = field(default=False)


@dataclass(frozen=True)
class Message(Dto):
    message: Optional[Text] = field(default=None)
    user_id: Optional[int] = field(default=None)
    chat_id: Optional[int] = field(default=None)
    thread_id: Optional[int] = field(default=None)

    sender: Optional[User] = field(default=None)

    @staticmethod
    def id() -> str:
        pass

    def sender_or_fail(self) -> User:
        if self.sender is None:
            raise ValueError(f'Sender not found')

        return self.sender
