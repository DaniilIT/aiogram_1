import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aioredis import redis
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, LOG_LEVEL, TG_TOKEN
from db import create_async_engine, get_session_maker
from handlers import commands_for_bot, register_user_commands
from middlewares import RegisterCheckMiddleware
from sqlalchemy.engine import URL

# пример
# https://github.com/MasterGroosha/telegram-report-bot/tree/7768165cd2339a91cafe0e953301d5f4f9c86e5d
# книга
# https://mastergroosha.github.io/aiogram-3-guide/

# router = Router()
#
#
# @router.message()
# async def echo_handler(message: types.Message):
#     try:
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         await message.answer('Nice try!')


async def main(logger: logging.Logger):
    # storage = MemoryStorage()
    storage = RedisStorage(redis=redis)
    dp = Dispatcher(storage=storage)

    dp.message.middleware(RegisterCheckMiddleware())
    dp.callback_query.middleware(RegisterCheckMiddleware())

    # dp.include_router(router)

    bot = Bot(token=TG_TOKEN, parse_mode='HTML')
    await bot.set_my_commands(commands=commands_for_bot)
    # await bot.set_chat_menu_button(
    #     menu_button=MenuButtonWebApp(
    #         text='Открыть веб приложение',
    #         web_app=WebAppInfo(url='https://google.com')
    #     )
    # )
    register_user_commands(dp)

    # postgres_url = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    postgres_url = URL.create(
        drivername='postgresql+asyncpg',
        username=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)
    # await proceed_schemas(async_engine, BaseModel.metadata)

    await dp.start_polling(bot, session_maker=session_maker, logger=logger)


if __name__ == '__main__':
    logging.basicConfig(level=LOG_LEVEL)
    logger = logging.getLogger(__name__)
    asyncio.run(main(logger))
    logging.info('Bot started')
