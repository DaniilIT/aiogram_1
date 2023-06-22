import enum
import logging
from typing import Optional

from db.base import Base, BaseModelMixin
from sqlalchemy import BIGINT, INTEGER, NUMERIC, TEXT, Column, Enum, ForeignKey, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import Mapped, relationship

# from .post_channel import PostChannel
# from .url import URL


class PRType(enum.Enum):
    """ Типы раскрутки
    """
    NONE = 0  # Оплата не установлена
    PUBLICATIONS = 1  # Оплата за одну публикацию
    CLICKS = 2  # Оплата за переход по ссылке


class Post(Base, BaseModelMixin):
    #     if TYPE_CHECKING:
    #         User = TypeVar('User')

    __tablename__ = 'posts'

    id: Mapped[int] = Column(INTEGER, primary_key=True)
    text: Mapped[str] = Column(TEXT, nullable=False)
    pr_type: Mapped[PRType] = Column(Enum(PRType), default=PRType.NONE)
    budget: Mapped[Optional[int]] = Column(INTEGER)
    pub_price: Mapped[Optional[float]] = Column(NUMERIC(precision=10, scale=2))
    url_price: Mapped[Optional[float]] = Column(NUMERIC(precision=10, scale=2))
    subs_min: Mapped[int] = Column(INTEGER, default=0)
    author_id: Mapped[int] = Column(BIGINT, ForeignKey('users.user_id'))

    author = relationship('User', back_populates='posts', lazy=True)

    #     # Каналы, на которых он был опубликован
    #     publicated_channel = relationship('Channel', secondary=PostChannel, back_populates="posts", lazy=False)

    def __str__(self):
        return f'<Post: {self.id}>'


async def get_post(post_id: int, session_maker: async_sessionmaker) -> Optional[Post]:
    async with session_maker() as session:
        async with session.begin():
            stmt = select(Post).where(Post.id == post_id)
            result = await session.execute(stmt)
            return result.scalars().unique().one_or_none()  # result.one_or_none()


async def create_post(
        session_maker: async_sessionmaker,
        text: str,
        author_id: int,
        pr_type: Optional[PRType] = None,
        budget: Optional[int] = None,
        pub_price: Optional[float] = None,
        url_price: Optional[float] = None,
        subs_min: Optional[int] = 0,
        # url: str = ''
) -> Post | None:
    async with session_maker() as session:
        async with session.begin():
            post = Post(
                text=text,
                author_id=author_id,
                pr_type=pr_type,
                budget=budget,
                subs_min=subs_min
            )
            # post.urls = [URL(url=text), ]
            if pub_price:
                post.pub_price = pub_price
            elif url_price:
                post.url_price = url_price

            try:
                session.add(post)
            except IntegrityError as e:
                logging.error(e)
            else:
                return post
