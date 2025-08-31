from datetime import date

from fastapi import APIRouter, HTTPException, Query, status

from src.api.dependencies import DBDep, UserIDDep
from src.schemas.booking import BookingAddSchema, BookingRequestAddSchema, BookingSchema

bookings_router = APIRouter(prefix='/bookings', tags=['Bookings'])


@bookings_router.get('/')
async def get_bookings(
    db: DBDep,
    _: UserIDDep,
    hotel_id: int = Query(),
    date_from: date = Query(examples=['2025-08-05']),
    date_to: date = Query(examples=['2025-08-08']),
) -> list[BookingSchema]:
    result = await db.bookings.get_filtered_by_date(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    return result


@bookings_router.get('/me')
async def get_user_bookings(db: DBDep, user_id: UserIDDep) -> list[BookingSchema]:
    return await db.bookings.get_filtered(user_id=user_id)


@bookings_router.post('/')
async def add_user_booking(db: DBDep, user_id: UserIDDep, booking_data: BookingRequestAddSchema) -> dict:
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Room with specifed room_id not found')
    create_data = BookingAddSchema(**booking_data.model_dump(), user_id=user_id, price=room.price)
    try:
        booking = await db.bookings.add_booking(create_data, room.hotel_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No available rooms')
    await db.commit()
    return {'status': 'OK', 'data': booking}
