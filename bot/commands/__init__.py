__all__ = ['commands_for_bot', 'register_user_commands']

from aiogram import F, Router  # magic filter
from aiogram.filters import Command, CommandStart
from aiogram.types import BotCommand
from middlewares.register_check import RegisterCheckMiddleware

from .callback_data_states import TestCallBackData
from .commands_info import commands_list
from .help import (
    call_clear_help_handler,
    call_help_handler,
    command_help_handler,
    func_help_handler,
)
from .settings import callback_settings_handler, command_settings_handler
from .start import command_start_handler

commands_for_bot = [BotCommand(command=cmd[0], description=cmd[1]) for cmd in commands_list]


def register_user_commands(router: Router):
    router.message.register(RegisterCheckMiddleware)
    router.callback_query.register(RegisterCheckMiddleware)

    router.message.register(command_help_handler, Command(commands=['help']))
    router.message.register(func_help_handler, F.text == 'Помощь')
    router.message.register(command_start_handler, CommandStart())  # Command(commands=['start'])
    router.message.register(command_start_handler, F.text == 'Старт')  # lambda message: message.text == 'hello'
    router.message.register(command_settings_handler, Command(commands=['settings']))

    router.callback_query.register(call_help_handler, F.data == 'help')  # из command_settings_handler
    router.callback_query.register(call_clear_help_handler, F.data == 'clear')
    router.callback_query.register(callback_settings_handler, TestCallBackData.filter())
