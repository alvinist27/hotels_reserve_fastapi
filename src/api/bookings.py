from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIDDep
from src.schemas.booking import BookingRequestAddSchema, BookingSchema, BookingAddSchema

bookings_router = APIRouter(prefix='/bookings', tags=['Bookings'])


@bookings_router.get('/')
async def get_user_bookings(db: DBDep, user_id: UserIDDep) -> list[BookingSchema]:
    return await db.bookings.get_all(user_id=user_id)


@bookings_router.post('/')
async def get_user_bookings(db: DBDep, user_id: UserIDDep, booking_data: BookingRequestAddSchema) -> dict:
    create_data = BookingAddSchema(**booking_data.model_dump(), user_id=user_id)
    booking = await db.bookings.add(create_data)
    await db.commit()
    return {'status': 'OK', 'data': booking}
