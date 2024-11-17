from pathlib import Path
from typing import Text

from dotenv import load_dotenv
from kink import Container, di

from sysarmy_bot.dependency_injection.bot_di import bot_bootstrap_di
from sysarmy_bot.dependency_injection.common import common_services_bootstrap_di
from sysarmy_bot.dependency_injection.help_di import help_bootstrap_di


async def bootstrap_di() -> Container:
    load_dotenv(dotenv_path=Path('.env'), override=True)

    await common_services_bootstrap_di()
    await bot_bootstrap_di()
    await help_bootstrap_di()
    return di


async def bootstrap_di_with_env_files(*args: Text) -> Container:
    for path in args:
        load_dotenv(dotenv_path=Path(path), override=True)

    return await bootstrap_di()
