from fastapi import APIRouter, Body, Query, status
from datetime import date
from src.api.dependencies import DBDep, PaginationDep
from src.schemas.hotels import HotelAddSchema, HotelPatchSchema

hotels_router = APIRouter(prefix='/hotels', tags=['Hotels'])


@hotels_router.get('/')
async def get_hotels(
    db: DBDep,
    pagination: PaginationDep,
    date_from: date = Query(example='2024-08-05'),
    date_to: date = Query(example='2024-08-08'),
    location: str | None = Query(None, description='Адрес отеля'),
    title: str | None = Query(None, description='Название отеля'),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_date(
        date_to=date_to,
        date_from=date_from,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1),
    )


@hotels_router.get('/{hotel_id}')
async def get_hotel(db: DBDep, hotel_id: int):
    return await db.hotels.get_one_or_none(id=hotel_id)


@hotels_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_hotel(db: DBDep, hotel_data: HotelAddSchema):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {'status': 'OK', 'data': hotel}


@hotels_router.put('/{hotel_id}')
async def update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAddSchema):
    await db.hotels.update(id=hotel_id, data=hotel_data)
    await db.commit()
    return {'status': 'OK'}


@hotels_router.patch('/{hotel_id}')
async def partial_update_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPatchSchema = Body(openapi_examples={
        '1': {
            'summary': 'Only title',
            'value': {
                'title': 'Отель Сочи 5 звезд у моря',
            }
        },
        '2': {
            'summary': 'Only location',
            'value': {
                'location': 'dubai_fountain',
            }
        },
        '3': {
            'summary': 'Location and Title',
            'value': {
                'location': 'dubai_fountain',
                'title': 'dubai Сочи 5 звезд у моря',
            }
        }
    })
):
    await db.hotels.update(id=hotel_id, exclude_unset=True, data=hotel_data)
    await db.commit()
    return {'status': 'OK'}


@hotels_router.delete('/{hotel_id}')
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {'status': 'OK'}
