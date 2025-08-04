from src.schemas.booking import BookingSchema

from src.models.bookings import BookingORM
from src.repositories.base import BaseRepository


class BookingRepository(BaseRepository):
    model = BookingORM
    schema = BookingSchema
