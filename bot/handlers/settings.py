from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from handlers.callback_data_states import TestCallBackData


async def command_settings_handler(message: types.Message):
    settings_builder = InlineKeyboardBuilder()
    settings_builder.button(text='Google', url='https://www.google.com')
    settings_builder.button(text='Помощь', callback_data='help')
    settings_builder.button(
        text='Помощь class',
        callback_data=TestCallBackData(text='Привет', user_id=message.from_user.id)
    )
    settings_builder.adjust(1, 2)
    await message.answer(
        'Настройки',
        # reply_markup=InlineKeyboardMarkup(inline_keyboard=settings_builder.export())
        reply_markup=settings_builder.as_markup()
    )


async def callback_settings_handler(call: types.CallbackQuery, callback_data: TestCallBackData):
    call.message.reply_markup.inline_keyboard.append([
        InlineKeyboardButton(text='Назад', callback_data='clear')
    ])
    # await call.message.answer( # ответить новым сообщением
    await call.message.edit_text(
        f'{callback_data.text}, {callback_data.user_id}',
        reply_markup=call.message.reply_markup  # оставить InlineKeyboard
    )
