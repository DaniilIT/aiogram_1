import datetime

from db.base import BaseModel
from sqlalchemy import DATE, INTEGER, VARCHAR, Column
from sqlalchemy.orm import Mapped


class User(BaseModel):
    __tablename__ = 'users'

    user_id: Mapped[int] = Column(INTEGER, primary_key=True)
    username: Mapped[str] = Column(VARCHAR(32))
    reg_date: Mapped[datetime.date] = Column(DATE, default=datetime.datetime.utcnow().date)  # datetime.date.today
    upd_date: Mapped[datetime.date] = Column(DATE, onupdate=datetime.datetime.utcnow().date)

    def __str__(self):
        return f'<User:{self.user_id}>'
