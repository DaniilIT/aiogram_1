from aiogram.types import Message


async def web_app_data_receive(message: Message):
    print(f'Проверка web_app_data_receive: {message.web_app_data.data}')
    await message.answer(message.web_app_data.data)
