import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types
from config import LOG_LEVEL, TG_TOKEN

from commands import commands_for_bot, register_user_commands

# пример
# https://github.com/MasterGroosha/telegram-report-bot/tree/7768165cd2339a91cafe0e953301d5f4f9c86e5d

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

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=LOG_LEVEL)
    asyncio.run(main())
