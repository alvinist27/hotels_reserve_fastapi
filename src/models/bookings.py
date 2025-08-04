from datetime import date

from sqlalchemy import Date, ForeignKey, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class BookingORM(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    room_id:  Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    date_from: Mapped[date] = mapped_column(Date())
    date_to: Mapped[date] = mapped_column(Date())
    price: Mapped[int] = mapped_column(Integer())

    @hybrid_property
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_from).days
