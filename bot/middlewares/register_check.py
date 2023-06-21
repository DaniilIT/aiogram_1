from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from db import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

# https://docs.aiogram.dev/en/dev-3.x/dispatcher/middlewares.html#class-based


class RegisterCheckMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: dict[str, Any]
    ) -> Any:
        session_maker: async_sessionmaker = data['session_maker']
        async with session_maker() as session:
            async with session.begin():
                stmt = select(User).where(User.user_id == event.from_user.id)
                result = await session.execute(stmt)
                user = result.one_or_none()

                if user is None:
                    user = User(
                        user_id=event.from_user.id,
                        username=event.from_user.username
                    )
                    # session.add(user)
                    await session.merge(user)

                    if isinstance(event, Message):
                        await event.answer('Ты успешно зарегистрирован(а)')
                    else:
                        await event.message.answer('Ты успешно зарегистрирован(а)')

        return await handler(event, data)
