from datetime import date

from pydantic import BaseModel
from sqlalchemy import select

from src.models.bookings import BookingORM
from src.models.rooms import RoomORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import get_rooms_ids_for_booking
from src.schemas.booking import BookingAddSchema


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

    async def add_booking(self, data: BookingAddSchema, hotel_id: int) -> BaseModel:
        rooms_ids_to_get = get_rooms_ids_for_booking(data.date_from, data.date_to, hotel_id)

        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book: list[int] = rooms_ids_to_book_res.scalars().all()

        if data.room_id not in rooms_ids_to_book:
            raise Exception
        return await self.add(data)
