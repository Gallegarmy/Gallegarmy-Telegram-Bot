from typing import Text

from sysarmy_bot.core.message import Message
from sysarmy_bot.core.test.faker_factory import FakerFactory
from sysarmy_bot.core.test.user_mother import create_random_user


def create_random_message_with_content(content: Text) -> Message:
    factory = FakerFactory()

    user = create_random_user()
    return Message(**{
        'sender': user,
        'message': content,
        'user_id': user.id,
        'chat_id': factory.new_faker().random_int(-1_000_000, 1_000_000),
        'thread_id': factory.new_faker().random_int(-1_000_000, 1_000_000),
    })
