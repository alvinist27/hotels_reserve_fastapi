from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIDDep
from src.exceptions import AllRoomsAreBookedException, AllRoomsAreBookedHTTPException
from src.schemas.bookings import BookingRequestAddSchema
from src.services.bookings import BookingService

bookings_router = APIRouter(prefix='/bookings', tags=['Bookings'])


@bookings_router.get('')
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@bookings_router.get('/me')
async def get_my_bookings(user_id: UserIDDep, db: DBDep):
    return await BookingService(db).get_my_bookings(user_id)


@bookings_router.post('', status_code=201)
async def add_booking(
    user_id: UserIDDep,
    db: DBDep,
    booking_data: BookingRequestAddSchema,
):
    try:
        booking = await BookingService(db).add_booking(user_id, booking_data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    return {'status': 'OK', 'data': booking}
