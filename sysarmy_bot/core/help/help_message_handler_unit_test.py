from typing import Dict, Text, Any
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, AsyncMock

from sysarmy_bot.config.administrators import InMemoryAdministratorsStorage
from sysarmy_bot.core.help.help_menu_composer import HelpMenuComposer
from sysarmy_bot.core.help.help_message_handler import HelpMessageHandler, HelpMessage
from sysarmy_bot.core.test.help.help_message_mother import create_help_message, create_admin_help_message
from sysarmy_bot.shared.logger import NullLogger
from sysarmy_bot.shared.message_sender import MessageSender, Message as Body


class TestHelpMessageHandler(IsolatedAsyncioTestCase):

    def setUp(self):
        self.help_menu_composer = HelpMenuComposer()
        self.logger = NullLogger()
        self.admins_repo = InMemoryAdministratorsStorage()

    def build_help_message_handler(self, sender: MessageSender) -> HelpMessageHandler:
        return HelpMessageHandler(self.logger, self.admins_repo, self.help_menu_composer, sender)

    def build_outgoing_message(self, incoming_message: HelpMessage, is_admin: bool) -> Dict[Text, Any]:
        return {
            'message': f"{self.help_menu_composer.compose(is_admin)}",
            'extra_args': {
                'chat_id': incoming_message.chat_id,
                'thread_id': incoming_message.thread_id
            }
        }

    @patch(f'{MessageSender.__module__}.{MessageSender.__name__}.send', new_callable=AsyncMock)
    async def test_handle_help_command_successfully_as_user(self, sender: AsyncMock) -> None:
        handler = self.build_help_message_handler(sender=sender)
        help_message = create_help_message()

        await handler.handle(help_message)

        message_to_send = self.build_outgoing_message(incoming_message=help_message, is_admin=False)
        sender.send.assert_awaited_with(message=Body(**message_to_send))

    @patch(f'{MessageSender.__module__}.{MessageSender.__name__}.send', new_callable=AsyncMock)
    async def test_handle_help_command_successfully_as_admin(self, sender: AsyncMock) -> None:
        # Given
        handler = self.build_help_message_handler(sender=sender)
        help_message = create_admin_help_message()

        await handler.handle(help_message)

        message_to_send = self.build_outgoing_message(incoming_message=help_message, is_admin=True)
        sender.send.assert_awaited_with(message=Body(**message_to_send))
