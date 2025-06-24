from fastapi import APIRouter, Body, Query, status

from src.api.dependencies import PaginationDep
from src.database import async_session
from src.repositories.hotels import HotelRepository
from src.schemas.hotels import HotelAddSchema, HotelPatchSchema

hotels_router = APIRouter(prefix='/hotels', tags=['Hotels'])


@hotels_router.get('/')
async def get_hotels(
    pagination: PaginationDep,
    location: str | None = Query(None, description='Адрес отеля'),
    title: str | None = Query(None, description='Название отеля'),
):
    per_page = pagination.per_page or 5
    async with async_session() as session:
        return await HotelRepository(session=session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )


@hotels_router.get('/{hotel_id}')
async def get_hotel(hotel_id: int):
    async with async_session() as session:
        return await HotelRepository(session=session).get_one_or_none(id=hotel_id)


@hotels_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_hotel(hotel_data: HotelAddSchema):
    async with async_session() as session:
        hotel = await HotelRepository(session).add(hotel_data)
        await session.commit()
    return {'status': 'OK', 'data': hotel}


@hotels_router.put('/{hotel_id}')
async def update_hotel(hotel_id: int, hotel_data: HotelAddSchema):
    async with async_session() as session:
        await HotelRepository(session).update(id=hotel_id, data=hotel_data)
        await session.commit()
    return {'status': 'OK'}


@hotels_router.patch('/{hotel_id}')
async def partial_update_hotel(
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
    async with async_session() as session:
        await HotelRepository(session).update(id=hotel_id, exclude_unset=True, data=hotel_data)
        await session.commit()
    return {'status': 'OK'}


@hotels_router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int):
    async with async_session() as session:
        await HotelRepository(session).delete(id=hotel_id)
        await session.commit()
    return {'status': 'OK'}
