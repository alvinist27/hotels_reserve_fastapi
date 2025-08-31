from datetime import date

from sqlalchemy import func, select

from src.models.bookings import BookingORM
from src.models.rooms import RoomORM


def get_rooms_ids_for_booking(date_from: date, date_to: date, hotel_id: int | None = None):
    rooms_count_cte = (
        select(BookingORM.room_id, func.count('*').label('quantity'))
        .select_from(BookingORM)
        .filter(
            BookingORM.date_from <= date_to,
            BookingORM.date_to >= date_from,
        )
        .group_by(BookingORM.room_id)
        .cte(name='rooms_count')
    )
    rooms_left_table_cte = (
        select(
            RoomORM.id.label('room_id'),
            (RoomORM.quantity - func.coalesce(rooms_count_cte.c.quantity, 0)).label('quantity'))
        .select_from(RoomORM)
        .outerjoin(rooms_count_cte, rooms_count_cte.c.room_id == RoomORM.id)
        .cte(name='rooms_left_table')
    )
    room_id_from_hotel = (
        select(RoomORM.id)
        .select_from(RoomORM)
    )
    if hotel_id:
        room_id_from_hotel = room_id_from_hotel.filter_by(hotel_id=hotel_id)
    room_id_from_hotel_subquery = room_id_from_hotel.subquery(name='hotel_subquery')

    room_ids_to_get = (
        select(rooms_left_table_cte.c.room_id)
        .select_from(rooms_left_table_cte)
        .where(
            rooms_left_table_cte.c.quantity > 0,
            rooms_left_table_cte.c.room_id.in_(room_id_from_hotel_subquery),
        )
    )
    return room_ids_to_get
