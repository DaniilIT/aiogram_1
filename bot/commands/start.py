from aiogram import types


async def command_start_handler(message: types.Message):
    await message.answer('Привет')
