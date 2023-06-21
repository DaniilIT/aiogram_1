from aiogram import types
from aiogram.utils.keyboard import (
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardBuilder,
)


async def command_start_handler(message: types.Message):
    # await message.answer('Привет')
    menu_builder = ReplyKeyboardBuilder()
    menu_builder.button(text='Помощь')
    menu_builder.add(
        KeyboardButton(text='Отправить контакт 1', request_contact=True),
        KeyboardButton(text='Отправить контакт 2', request_location=True)
    )
    menu_builder.row(
        KeyboardButton(text='Отправить голосование 1', request_poll=KeyboardButtonPollType()),
        KeyboardButton(text='Отправить голосование 2', request_poll=KeyboardButtonPollType(type='quiz'))
    )
    # menu_builder.adjust(2, 2, 1)
    await message.answer(
        'Меню',
        # reply_markup=ReplyKeyboardMarkup(keyboard=menu_builder.export())  # deprecated
        reply_markup=menu_builder.as_markup(resize_keyboard=True)
    )
