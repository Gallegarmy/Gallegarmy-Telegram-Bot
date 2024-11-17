from pytest import mark

from telethon import TelegramClient


@mark.asyncio
async def test_receive_help_from_bot_as_user(telegram_client: TelegramClient):
    async with telegram_client.conversation('@telebowling_support_bot', total_timeout=10) as conv:
        await conv.send_message('/help')

        response = await conv.get_response()
        print(response)
        assert response.text == '/help'

