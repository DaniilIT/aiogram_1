from aiogram import types
from db.post import get_post
from sqlalchemy.ext.asyncio import async_sessionmaker
from structures import keyboards
from structures.callback_data_factories import PostCD


async def menu_posts_get(call: types.CallbackQuery, callback_data: PostCD, session_maker: async_sessionmaker):
    post = await get_post(post_id=callback_data.post_id, session_maker=session_maker)
    await call.message.edit_text(
        '<b>Пост</b>\n\n{text}\n\n<s>---</s>'.format(text=post.text),
        reply_markup=keyboards.POSTS_BOARD
    )
