__all__ = ['commands_for_bot', 'register_user_commands']

from aiogram import F, Router  # magic filter
from aiogram.filters import Command, CommandStart
from aiogram.types import BotCommand

from .commands_info import commands_list
from .help import command_help_handler
from .start import command_start_handler

commands_for_bot = [BotCommand(command=cmd[0], description=cmd[1]) for cmd in commands_list]


def register_user_commands(router: Router):
    router.message.register(command_help_handler, Command(commands=['help']))
    router.message.register(command_start_handler, CommandStart())  # Command(commands=['start'])
    router.message.register(command_start_handler, F.text == 'Старт')  # lambda message: message.text == 'hello'
