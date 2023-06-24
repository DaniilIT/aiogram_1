import asyncio

import pytest
import pytest_asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import register_user_commands
from tests.mocked_bot import MockedBot


@pytest_asyncio.fixture(scope='session')
async def memory_storage():
    storage = MemoryStorage()
    try:
        yield storage
    finally:
        await storage.close()


@pytest.fixture(scope='session')
def bot():
    bot = MockedBot()
    token = Bot.set_current(bot)
    try:
        yield bot
    finally:
        Bot.reset_current(token)


@pytest_asyncio.fixture(scope='session')
async def dispatcher():
    dp = Dispatcher()
    register_user_commands(dp)
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()


# https://github.com/tortoise/tortoise-orm/issues/638
@pytest.fixture(scope='session')
def event_loop():
    return asyncio.get_event_loop()
