from datetime import date

from sqlalchemy import select

from src.models.bookings import BookingORM
from src.models.rooms import RoomORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import get_rooms_ids_for_booking


class BookingRepository(BaseRepository):
    model = BookingORM
    mapper = BookingDataMapper

    async def get_filtered_by_date(self, hotel_id: int, date_from: date, date_to: date):
        rooms_ids_to_get = get_rooms_ids_for_booking(date_from, date_to, hotel_id)
        return await self.get_filtered(RoomORM.id.in_(rooms_ids_to_get))

    async def get_bookings_with_today_checkin(self):
        query = (
            select(self.model)
            .filter(self.model.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]
