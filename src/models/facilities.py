import typing

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models import RoomORM


class FacilityORM(Base):
    __tablename__ = 'facilities'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    rooms: Mapped[list['RoomORM']] = relationship(
        back_populates='facilities',
        secondary='room_facilities',
    )


class RoomFacilityORM(Base):
    __tablename__ = 'room_facilities'

    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'), primary_key=True)
    facility_id: Mapped[int] = mapped_column(ForeignKey('facilities.id'), primary_key=True)
