from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardMarkup

MENU_BOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Твои посты'),
            KeyboardButton(text='Твои каналы')
        ],
        [
            KeyboardButton(text='Аккаунт'),
            KeyboardButton(
                text='WebApp',  # https://github.com/MassonNN/just-test-pages
                web_app=WebAppInfo(url='https://massonnn.github.io/just-test-pages/')
            )
        ]
    ],
    resize_keyboard=True
)
