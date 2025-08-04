from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import DBDep, UserIDDep
from src.schemas.booking import BookingAddSchema, BookingRequestAddSchema, BookingSchema

bookings_router = APIRouter(prefix='/bookings', tags=['Bookings'])


@bookings_router.get('/')
async def get_bookings(db: DBDep, _: UserIDDep) -> list[BookingSchema]:
    return await db.bookings.get_all()


@bookings_router.get('/me')
async def get_user_bookings(db: DBDep, user_id: UserIDDep) -> list[BookingSchema]:
    return await db.bookings.get_filtered(user_id=user_id)


@bookings_router.post('/')
async def get_user_bookings(db: DBDep, user_id: UserIDDep, booking_data: BookingRequestAddSchema) -> dict:
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Room with specifed room_id not found')
    create_data = BookingAddSchema(**booking_data.model_dump(), user_id=user_id, price=room.price)
    booking = await db.bookings.add(create_data)
    await db.commit()
    return {'status': 'OK', 'data': booking}
