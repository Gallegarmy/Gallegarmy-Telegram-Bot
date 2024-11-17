from telethon import TelegramClient


def create_bot_telegram_client(
        app_id: int,
        app_hash: str,
) -> TelegramClient:
    return TelegramClient(None, app_id, app_hash)
