from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardMarkup

# def cancel_board() -> ReplyKeyboardMarkup:
#     board = ReplyKeyboardBuilder()
#     board.button('Отмена')
#     return board.as_markup(resize_keyboard=True)

CANCEL_BOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отмена')]
    ],
    resize_keyboard=True
)
