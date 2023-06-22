from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from db.post import Post
from structures.callback_data_factories import PostCD, PostCDAction

POSTS_BOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Посмотреть статистику', callback_data=PostCD(action=PostCDAction.STATS).pack()),
            InlineKeyboardButton(text='Рекламировать', callback_data=PostCD(action=PostCDAction.PR).pack())
        ],
        [
            InlineKeyboardButton(text='Удалить', callback_data=PostCD(action=PostCDAction.DELETE).pack()),
            InlineKeyboardButton(text='Назад', callback_data='menu')
        ]
    ]
    # resize_keyboard=True
)


def generate_posts_board(posts: list[Post]) -> InlineKeyboardMarkup:
    """ Сгенерировать клавиатуру с постами
    """
    builder = InlineKeyboardBuilder()
    for post in posts:
        builder.button(
            text=post.text[:20],
            callback_data=PostCD(action=PostCDAction.GET, post_id=post.id).pack()
        )
    builder.button(
        text='Создать пост',
        callback_data=PostCD(action=PostCDAction.CREATE).pack()
    )
    builder.adjust(1)
    return builder.as_markup()
