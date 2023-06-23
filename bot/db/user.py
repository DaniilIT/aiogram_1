from typing import Optional

from db.base import Base, BaseModelMixin
from sqlalchemy import BIGINT, VARCHAR, Column, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import Mapped, relationship, selectinload


class User(Base, BaseModelMixin):
    __tablename__ = 'users'

    user_id: Mapped[int] = Column(BIGINT, primary_key=True)
    username: Mapped[str] = Column(VARCHAR(32), unique=True)
    posts = relationship('Post', back_populates='author', lazy=True)  # select / joined

    def __str__(self):
        return f'<User: {self.user_id}>'


async def get_user(user_id: int, session_maker: async_sessionmaker) -> Optional[User]:
    async with session_maker() as session:
        async with session.begin():
            # options(joinedload(User.posts))
            stmt = select(User).options(selectinload(User.posts)).where(User.user_id == user_id)
            result = await session.execute(stmt)
            # user = result.one_or_none()
            return result.scalars().one_or_none()


async def create_user(user_id: int, username: str, session_maker: async_sessionmaker) -> Optional[User]:
    async with session_maker() as session:
        async with session.begin():
            user = User(
                user_id=user_id,
                username=username
            )
            try:
                await session.merge(user)
                # session.add(user)
            except IntegrityError:
                pass

    return user
