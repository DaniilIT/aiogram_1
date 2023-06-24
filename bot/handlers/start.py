from contextlib import suppress

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from db.user import get_user
from sqlalchemy.ext.asyncio import async_sessionmaker
from structures import keyboards
from structures.fsm_groups import PostStates

# async def command_start_handler(message: Message):
#     # await message.answer('Привет')
#     menu_builder = ReplyKeyboardBuilder()
#     menu_builder.button(text='Помощь')
#     menu_builder.add(
#         KeyboardButton(text='Отправить контакт 1', request_contact=True),
#         KeyboardButton(text='Отправить контакт 2', request_location=True)
#     )
#     menu_builder.row(
#         KeyboardButton(text='Отправить голосование 1', request_poll=KeyboardButtonPollType()),
#         KeyboardButton(text='Отправить голосование 2', request_poll=KeyboardButtonPollType(type='quiz'))
#     )
#     # menu_builder.adjust(2, 2, 1)
#     await message.answer(
#         'Меню',
#         # reply_markup=ReplyKeyboardMarkup(keyboard=menu_builder.export())  # deprecated
#         reply_markup=menu_builder.as_markup(resize_keyboard=True)
#     )


async def command_start_handler(message: Message) -> Message:
    return await message.answer(
        'Меню',
        reply_markup=keyboards.MENU_BOARD
    )


async def call_start_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    with suppress(Exception):
        await call.message.delete()
    await call.message.answer(
        'Меню',
        reply_markup=keyboards.MENU_BOARD
    )


async def command_posts_handler(message: Message, session_maker: async_sessionmaker, state: FSMContext):
    user = await get_user(message.from_user.id, session_maker)
    await message.answer(
        'Твои посты',
        reply_markup=keyboards.generate_posts_board(posts=user.posts)
    )
    await state.set_state(PostStates.waiting_for_select)


async def command_channels_handler(message: Message):
    await message.answer(
        'Твои каналы'
    )


async def command_account_handler(message: Message):
    await message.answer(
        'Аккаунт'
    )
