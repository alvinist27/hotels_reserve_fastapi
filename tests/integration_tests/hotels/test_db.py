from src.schemas.hotels import HotelAddSchema


async def test_add_hotel(db):
    hotel_data = HotelAddSchema(title="Hotel 5 stars", location="Сочи")
    await db.hotels.add(hotel_data)
    await db.commit()
