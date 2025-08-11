from datetime import date

from sqlalchemy import select

from src.models.hotels import HotelORM
from src.models.rooms import RoomORM
from src.repositories.base import BaseRepository
from src.repositories.utils import get_rooms_ids_for_booking
from src.schemas.hotels import HotelSchema


class HotelRepository(BaseRepository):
    model = HotelORM
    schema = HotelSchema

    async def get_filtered_by_date(
        self,
        date_from: date,
        date_to: date,
        location: str,
        title: str,
        limit: int,
        offset: int,
    ) -> list:
        rooms_ids_to_get = get_rooms_ids_for_booking(date_from, date_to)
        hotels_ids_to_get = (
            select(RoomORM.hotel_id)
            .select_from(RoomORM)
            .where(RoomORM.id.in_(rooms_ids_to_get))
        )
        if location:
            hotels_ids_to_get = hotels_ids_to_get.filter(self.model.location.icontains(location.strip()))
        if title:
            hotels_ids_to_get = hotels_ids_to_get.filter(self.model.title.icontains(title.strip()))
        hotels_ids_to_get = (
            hotels_ids_to_get
            .limit(limit)
            .offset(offset)
        )
        return await self.get_filtered(HotelORM.id.in_(hotels_ids_to_get))
