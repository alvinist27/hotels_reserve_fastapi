from datetime import date

from src.models.bookings import BookingORM
from src.models.rooms import RoomORM
from src.repositories.base import BaseRepository
from src.repositories.utils import get_rooms_ids_for_booking
from src.schemas.booking import BookingSchema


class BookingRepository(BaseRepository):
    model = BookingORM
    schema = BookingSchema

    async def get_filtered_by_date(self, hotel_id: int, date_from: date, date_to: date):
        rooms_ids_to_get = get_rooms_ids_for_booking(date_from, date_to, hotel_id)
        return await self.get_filtered(RoomORM.id.in_(rooms_ids_to_get))
