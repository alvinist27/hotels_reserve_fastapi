from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import UniqueConstraint

from src.database import Base


class HotelORM(Base):
    __tablename__ = 'hotels'
    __table_args__ = (
        UniqueConstraint('title', 'location', name='uq_hotel_title_location'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str]
