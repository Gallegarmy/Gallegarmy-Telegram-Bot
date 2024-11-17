from dataclasses import asdict
from typing import Text

from sysarmy_bot.core.message import User
from sysarmy_bot.core.test.faker_factory import FakerFactory


def create_random_user() -> User:
    factory = FakerFactory()

    return User(**{
        'id': factory.new_faker().random_int(-1_000_000, 1_000_000),
        'first_name': factory.new_faker().first_name(),
        'last_name': factory.new_faker().last_name(),
        'username': factory.new_faker().user_name(),
        'language_iso2': factory.new_faker().language_code().upper(),
        'is_bot': False,
    })


def create_user_with_name_and_username(name: Text, username: Text) -> User:
    random_user = create_random_user()
    return User(**{**asdict(random_user), 'first_name': name, 'username':username, 'is_bot': False})