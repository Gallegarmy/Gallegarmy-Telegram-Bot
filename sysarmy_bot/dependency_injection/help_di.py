from kink import di

from sysarmy_bot.config.administrators import InMemoryAdministratorsStorage
from sysarmy_bot.core.help.help_menu_composer import HelpMenuComposer
from sysarmy_bot.core.help.help_message_handler import HelpMessage, HelpMessageHandler
from sysarmy_bot.shared.logger import Logger
from sysarmy_bot.shared.message_bus import MessageBus
from sysarmy_bot.shared.message_sender import MessageSender


async def help_bootstrap_di() -> None:
    message_bus, logger, admins_repo, message_sender = (
        di[MessageBus],
        di[Logger],
        di[InMemoryAdministratorsStorage],
        di[MessageSender],
    )

    await message_bus.register_message_handler(
        message=HelpMessage,
        handler=HelpMessageHandler(
            logger=logger,
            admins_repo=admins_repo,
            help_menu_composer=HelpMenuComposer(),
            sender=message_sender
        )
    )
