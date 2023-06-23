from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from aioredis import redis
from db.user import create_user, get_user
from sqlalchemy.ext.asyncio import async_sessionmaker

# https://docs.aiogram.dev/en/dev-3.x/dispatcher/middlewares.html#class-based


class RegisterCheckMiddleware(BaseMiddleware):
    """ Вызывается каждый раз при отправке сообщения и нажатии inline-кнопки
    """

    def __init__(self, *args, **kwargs):
        pass

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: dict[str, Any]
    ) -> Any:
        if isinstance(event, Message) and event.web_app_data:
            return await handler(event, data)

        user = event.from_user
        session_maker: async_sessionmaker = data['session_maker']

        if not await redis.get(name='new_user' + str(user.id)):
            new_user = None

            if not await get_user(user.id, session_maker):
                new_user = await create_user(
                    user_id=user.id,
                    username=user.username,
                    session_maker=session_maker
                )

                # await data['bot'].send_message(user.id, 'Ты успешно зарегистрирован(а)')

                if isinstance(event, Message):
                    await event.answer('Ты успешно зарегистрирован(а)')
                else:
                    await event.message.answer('Ты успешно зарегистрирован(а)')

            await redis.set(
                name='new_user' + str(user.id),
                value='true' if new_user else 'false'
            )

        return await handler(event, data)
