from datetime import date, datetime

from sqlalchemy import DATE, Column
from sqlalchemy.orm import Mapped, declarative_base

Base = declarative_base()


class BaseModelMixin:
    reg_date: Mapped[date] = Column(DATE, default=datetime.utcnow().date)  # date.today
    upd_date: Mapped[date] = Column(DATE, onupdate=datetime.utcnow().date)

    @property
    def no_upd_days(self) -> int:
        """ Количество дней, которое модель не обновлялась
        """
        date_delta = datetime.utcnow().date() - self.upd_date
        return date_delta.days
