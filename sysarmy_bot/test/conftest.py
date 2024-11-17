import asyncio
import tracemalloc
from typing import Generator

import pytest
from kink import Container
from telethon import TelegramClient

from sysarmy_bot.dependency_injection import bootstrap_di_with_env_files
from sysarmy_bot.shared.environment_var_getter import EnvironmentVarGetter


@pytest.fixture(scope="session")
async def event_loop(request) -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop()

    try:
        yield loop
        loop.close()
    except BaseException:
        pass


@pytest.fixture(scope='session')
async def app() -> Container:
    tracemalloc.start()
    container = await bootstrap_di_with_env_files('.env', '.env.test')
    yield container


@pytest.fixture(scope='session')
async def telegram_client(app: Container) -> TelegramClient:
    client, env = app[TelegramClient], app[EnvironmentVarGetter]

    assert isinstance(client, TelegramClient)

    await client.connect()
    await client.start()

    yield client

    await client.disconnect()
    await client.disconnected
