from sysarmy_bot.config.administrators import InMemoryAdministratorsStorage
from sysarmy_bot.core.help.help_message_handler import HelpMessage
from sysarmy_bot.core.test.message_mother import create_random_message_with_content
from sysarmy_bot.core.test.user_mother import create_user_with_name_and_username


def create_help_message() -> HelpMessage:
    message = create_random_message_with_content('/help')
    return HelpMessage(
        message=message.message,
        user_id=message.user_id,
        chat_id=message.chat_id,
        thread_id=message.thread_id,
        sender=message.sender,
    )


def create_admin_help_message() -> HelpMessage:
    message = create_random_message_with_content('/help')
    user = InMemoryAdministratorsStorage().fetch_one_randomly()
    admin_user = create_user_with_name_and_username(name=user.name, username=user.username)

    return HelpMessage(
        message=message.message,
        user_id=admin_user.id,
        chat_id=message.chat_id,
        thread_id=message.thread_id,
        sender=admin_user,
    )
