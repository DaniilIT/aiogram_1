__all__ = ['commands_for_bot', 'register_user_commands']

from aiogram import F, Router  # magic filter
from aiogram.enums import ContentType
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import any_state
from aiogram.types import BotCommand
from structures.callback_data_factories import PostCD, PostCDAction
from structures.fsm_groups import PostStates

from .callback_data_states import TestCallBackData
from .commands_info import commands_list
from .create_post import (
    menu_posts_create,
    menu_posts_create_prtype,
    menu_posts_create_prtype_pub,
    menu_posts_create_prtype_url,
    menu_posts_create_subs_min,
    menu_posts_create_text,
    menu_posts_create_url,
)
from .get_post import menu_posts_get
from .help import (
    call_clear_help_handler,
    call_help_handler,
    command_help_handler,
    func_help_handler,
)
from .settings import callback_settings_handler, command_settings_handler
from .start import (
    call_start_handler,
    command_account_handler,
    command_channels_handler,
    command_posts_handler,
    command_start_handler,
)
from .web_app_data import web_app_data_receive

commands_for_bot = [BotCommand(command=cmd[0], description=cmd[1]) for cmd in commands_list]


def register_user_commands(router: Router):
    # router.message.register(RegisterCheckMiddleware)
    # router.callback_query.register(RegisterCheckMiddleware)

    router.message.register(command_help_handler, Command(commands=['help']))
    router.message.register(func_help_handler, F.text == 'Помощь')
    router.message.register(command_start_handler, CommandStart())  # Command(handlers=['start'])
    router.message.register(command_start_handler, F.text == 'Старт')  # lambda message: message.text == 'hello'
    router.message.register(command_settings_handler, Command(commands=['settings']))

    router.message.register(command_posts_handler, F.text == 'Твои посты')
    router.message.register(command_channels_handler, F.text == 'Твои каналы')
    router.message.register(command_account_handler, F.text == 'Аккаунт')

    # router.message.register(menu_posts_create, F.data == 'createpost', PostStates.waiting_for_select)
    # router.message.register(menu_posts_get, F.data.startswith == 'getpost', PostStates.waiting_for_select)
    router.callback_query.register(menu_posts_create,
                                   PostCD.filter(F.action == PostCDAction.CREATE), PostStates.waiting_for_select)
    router.callback_query.register(menu_posts_get,
                                   PostCD.filter(F.action == PostCDAction.GET), PostStates.waiting_for_select)

    router.message.register(menu_posts_create_text, PostStates.waiting_for_text)
    router.message.register(menu_posts_create_subs_min, PostStates.waiting_for_post_subs_min)
    router.message.register(menu_posts_create_prtype_url, PostStates.waiting_for_price_url)
    router.message.register(menu_posts_create_prtype_pub, PostStates.waiting_for_price_publication)
    router.message.register(menu_posts_create_prtype, PostStates.waiting_for_pr_type)
    router.message.register(menu_posts_create_url, PostStates.waiting_for_url)

    router.message.register(web_app_data_receive, F.content_type.in_(ContentType.WEB_APP_DATA, ))

    router.callback_query.register(call_start_handler, F.data == 'menu', any_state)
    router.callback_query.register(call_help_handler, F.data == 'help')  # из command_settings_handler
    router.callback_query.register(call_clear_help_handler, F.data == 'clear')
    router.callback_query.register(callback_settings_handler, TestCallBackData.filter())
