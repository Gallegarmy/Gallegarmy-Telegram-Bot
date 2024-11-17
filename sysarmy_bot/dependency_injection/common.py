from kink import di, Container
from telethon import TelegramClient

from sysarmy_bot.config import Config
from sysarmy_bot.config.administrators import InMemoryAdministratorsStorage
from sysarmy_bot.shared.environment_var_getter import OSEnvironmentVarGetter, EnvironmentVarGetter
from sysarmy_bot.shared.logger import JsonStructuredLogger, Logger
from sysarmy_bot.shared.message_bus import AwaitableMessageBus, MessageBus
from sysarmy_bot.shared.telethon_utils import create_bot_telegram_client


async def common_services_bootstrap_di() -> None:
    di[EnvironmentVarGetter] = OSEnvironmentVarGetter()
    di[Config] = Config.from_yaml(
        env=di[EnvironmentVarGetter].get_or_fail('APP_ENV'),
        config_file_path='./config/config.yaml'
    )
    di[Logger] = JsonStructuredLogger()
    di[InMemoryAdministratorsStorage] = InMemoryAdministratorsStorage()
    di[MessageBus] = AwaitableMessageBus(logger=di[Logger])
    di[TelegramClient] = None

    if di[Config].environment.is_testing():
        await __init_common_services_testing(di)


async def __init_common_services_testing(container: Container) -> None:
    env = container[EnvironmentVarGetter]
    app_id, app_hash = (
        env.get_or_fail('TELEGRAM_APP_ID'),
        env.get_or_fail('TELEGRAM_APP_HASH'),
    )

    container[TelegramClient] = create_bot_telegram_client(
        app_id=int(app_id),
        app_hash=app_hash,
    )
