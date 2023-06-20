from aiogram import types
from aiogram.filters import CommandObject

from . import commands_list


async def command_help_handler(message: types.Message, command: CommandObject):
    if command.args:
        for cmd in commands_list:
            if cmd[0] == command.args:
                return await message.answer(
                    f'{cmd[0]} – {cmd[1]}\n\n{cmd[2]}'
                )
        return await message.answer('Команда не найдена')
    return await message.answer(
        'Помощь и справка о боте\n'
        'Для того, чтобы получить информацию о команде используй /help <команда>'
    )
