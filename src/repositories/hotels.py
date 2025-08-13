from datetime import date

from sqlalchemy import select

from src.models.hotels import HotelORM
from src.models.rooms import RoomORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.utils import get_rooms_ids_for_booking


class HotelRepository(BaseRepository):
    model = HotelORM
    mapper = HotelDataMapper

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
        query = select(HotelORM).filter(HotelORM.id.in_(hotels_ids_to_get))
        if location:
            query = query.filter(self.model.location.icontains(location.strip()))
        if title:
            query = query.filter(self.model.title.icontains(title.strip()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(row) for row in result.scalars().all()]
