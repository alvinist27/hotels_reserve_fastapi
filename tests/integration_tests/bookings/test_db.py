from datetime import date

from src.schemas.booking import BookingAddSchema


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAddSchema(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
        price=100,
    )
    booking = await db.bookings.add(booking_data)
    booking_from_db = await db.bookings.get_one_or_none(id=booking.id)
    assert booking_from_db is not None
    booking_data.price = 1000
    await db.bookings.update(booking_data, id=booking_from_db.id)
    assert (await db.bookings.get_one_or_none(id=booking_from_db.id)).price == 1000
    await db.bookings.delete(id=booking.id)
    assert (await db.bookings.get_one_or_none(id=booking_from_db.id)) is None
    await db.commit()
