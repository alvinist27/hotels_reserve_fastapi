from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, PaginationDep
from src.exceptions import HotelNotFoundHTTPException, ObjectNotFoundException
from src.schemas.hotels import HotelAddSchema, HotelPatchSchema
from src.services.hotels import HotelService

hotels_router = APIRouter(prefix='/hotels', tags=['Hotels'])


@hotels_router.get('')
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description='Локация'),
    title: str | None = Query(None, description='Название отеля'),
    date_from: date = Query(examples=['2024-08-01']),
    date_to: date = Query(examples=['2024-08-10']),
):
    return await HotelService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )


@hotels_router.get('/{hotel_id}')
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@hotels_router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAddSchema = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи 5 звезд у моря",
                    "location": "ул. Моря, 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Дубай У фонтана",
                    "location": "ул. Шейха, 2",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {'status': 'OK', 'data': hotel}


@hotels_router.put('/{hotel_id}')
async def edit_hotel(hotel_id: int, hotel_data: HotelAddSchema, db: DBDep):
    await HotelService(db).edit_hotel(hotel_id, hotel_data)
    return {'status': 'OK'}


@hotels_router.patch('/{hotel_id}')
async def partially_edit_hotel(
    hotel_id: int,
    hotel_data: HotelPatchSchema,
    db: DBDep,
):
    await HotelService(db).edit_hotel_partially(hotel_id, hotel_data, exclude_unset=True)
    return {'status': 'OK'}


@hotels_router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id)
    return {'status': 'OK'}
