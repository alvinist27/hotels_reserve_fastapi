from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class FacilityORM(Base):
    __tablename__ = 'facilities'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))


class RoomFacilityORM(Base):
    __tablename__ = 'room_facilities'

    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'), primary_key=True)
    facility_id: Mapped[int] = mapped_column(ForeignKey('facilities.id'), primary_key=True)
