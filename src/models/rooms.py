from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class RoomORM(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]

    facilities: Mapped[list['FacilityORM']] = relationship(
        back_populates='rooms',
        secondary='room_facilities',
    )
