from aiogram import types
from aiogram.filters import CommandObject
from aiogram.utils.keyboard import InlineKeyboardButton
from handlers.commands_info import commands_list


async def command_help_handler(message: types.Message, command: CommandObject):
    if command.args:
        for cmd in commands_list:
            if cmd[0] == command.args:
                return await message.answer(
                    f'{cmd[0]} – {cmd[1]}\n\n{cmd[2]}'
                )
        return await message.answer('Команда не найдена')

    return await func_help_handler(message)


async def func_help_handler(message: types.Message):
    return await message.answer(
        'Помощь и справка о боте\n'
        'Для того, чтобы получить информацию о команде используй /help <команда>'
    )


async def call_help_handler(call: types.CallbackQuery):
    call.message.reply_markup.inline_keyboard.append([
        InlineKeyboardButton(text='Назад', callback_data='clear')
    ])
    # await call.message.answer(  # ответить новым сообщением
    await call.message.edit_text(
        'Помощь и справка о боте\n'
        'Для того, чтобы получить информацию о команде используй /help <команда>',
        reply_markup=call.message.reply_markup  # оставить InlineKeyboard
    )


async def call_clear_help_handler(call: types.CallbackQuery):
    call.message.reply_markup.inline_keyboard.pop()
    await call.message.edit_text(
        'Настройки',
        # reply_markup=call.message.reply_markup  # оставить InlineKeyboard
        reply_markup=call.message.reply_markup
    )
