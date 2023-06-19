__all__ = ['register_user_commands']

from aiogram import Router
from aiogram.filters import CommandStart

from .start import command_start_handler


def register_user_commands(router: Router):
    router.message.register(command_start_handler, CommandStart())  # Command(commands=['start'])
