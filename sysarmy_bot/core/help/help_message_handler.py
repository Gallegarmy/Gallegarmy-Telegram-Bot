from dataclasses import dataclass

from sysarmy_bot.config.administrators import InMemoryAdministratorsStorage
from sysarmy_bot.core.help.help_menu_composer import HelpMenuComposer
from sysarmy_bot.core.message import Message
from sysarmy_bot.shared.logger import Logger
from sysarmy_bot.shared.message_bus import MessageHandler
from sysarmy_bot.shared.message_sender import MessageSender, Message as Body


@dataclass(frozen=True)
class HelpMessage(Message):

    @staticmethod
    def id() -> str:
        return 'help_message'


class HelpMessageHandler(MessageHandler):

    def __init__(
            self,
            logger: Logger,
            admins_repo: InMemoryAdministratorsStorage,
            help_menu_composer: HelpMenuComposer,
            sender: MessageSender,
    ):
        self.logger = logger
        self.admins_repo = admins_repo
        self.sender = sender
        self.help_menu_composer = help_menu_composer

    async def handle(self, message: HelpMessage) -> None:
        writer = message.sender_or_fail()
        writer_is_admin = self.admins_repo.exists_by_handle(writer.username)

        message_to_send = {
            'message': f"{self.help_menu_composer.compose(writer_is_admin)}",
            'extra_args': {
                'chat_id': message.chat_id,
                'thread_id': message.thread_id
            }
        }

        if writer_is_admin:
            self.logger.info("Admin help requested", user_id=writer.id, username=writer.username)
            await self.sender.send(message=Body(**message_to_send))
            return

        self.logger.info("User help requested", user_id=writer.id, username=writer.username)
        await self.sender.send(message=Body(**message_to_send))
