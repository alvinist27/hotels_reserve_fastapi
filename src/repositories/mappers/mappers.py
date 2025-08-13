from src.models.bookings import BookingORM
from src.models.facilities import FacilityORM
from src.models.hotels import HotelORM
from src.models.rooms import RoomORM
from src.models.users import UserORM
from src.repositories.mappers.base import DataMapper
from src.schemas.booking import BookingSchema
from src.schemas.facilities import FacilitySchema
from src.schemas.hotels import HotelSchema
from src.schemas.rooms import RoomSchema, RoomWithRels
from src.schemas.users import UserSchema


class HotelDataMapper(DataMapper):
    db_model = HotelORM
    schema = HotelSchema


class RoomDataMapper(DataMapper):
    db_model = RoomORM
    schema = RoomSchema


class RoomWithRelsDataMapper(DataMapper):
    db_model = RoomORM
    schema = RoomWithRels


class UserDataMapper(DataMapper):
    db_model = UserORM
    schema = UserSchema


class BookingDataMapper(DataMapper):
    db_model = BookingORM
    schema = BookingSchema


class FacilityDataMapper(DataMapper):
    db_model = FacilityORM
    schema = FacilitySchema
