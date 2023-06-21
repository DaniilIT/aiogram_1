import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types
from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER, LOG_LEVEL, TG_TOKEN
from db import BaseModel, create_async_engine, get_session_maker, proceed_schemas
from sqlalchemy.engine import URL

from commands import commands_for_bot, register_user_commands

# пример
# https://github.com/MasterGroosha/telegram-report-bot/tree/7768165cd2339a91cafe0e953301d5f4f9c86e5d
# книга
# https://mastergroosha.github.io/aiogram-3-guide/

router = Router()


@router.message()
async def echo_handler(message: types.Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer('Nice try!')


async def main():
    dp = Dispatcher()
    dp.include_router(router)

    bot = Bot(token=TG_TOKEN)

    register_user_commands(dp)
    await bot.set_my_commands(commands=commands_for_bot)

    # postgres_url = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    postgres_url = URL.create(
        drivername='postgresql+asyncpg',
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)  # noqa F841
    await proceed_schemas(async_engine, BaseModel.metadata)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=LOG_LEVEL)
    asyncio.run(main())
