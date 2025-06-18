from typing import Any

from fastapi import APIRouter, Body, HTTPException, Query
from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.database import async_session
from src.models.hotels import HotelModel
from src.schemas.hotels import HotelPatchSchema, HotelSchema

hotels_router = APIRouter(prefix='/hotels', tags=['Hotels'])


def get_hotel_to_update(hotel_id: int) -> dict[str, Any]:
    hotel_to_update = None
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel_to_update = hotel
    if not hotel_to_update:
        raise HTTPException(status_code=404, detail='Hotel not found')
    return hotel_to_update


@hotels_router.get('/')
async def get_hotels(
    pagination: PaginationDep,
    location: str | None = Query(None, description='Адрес отеля'),
    title: str | None = Query(None, description='Название отеля'),
):
    current_offset = (pagination.page-1) * pagination.per_page
    async with async_session() as session:
        hotels_query = select(HotelModel)
        if location:
            hotels_query = hotels_query.where(HotelModel.location.ilike(f'%{location}%'))
        if title:
            hotels_query = hotels_query.where(HotelModel.title.ilike(f'%{title}%'))
        hotels_query = (
            hotels_query
            .limit(limit=current_offset+pagination.per_page)
            .offset(offset=current_offset)
        )
        result = await session.execute(hotels_query)
        hotels = result.scalars().all()
        return hotels


@hotels_router.post('/')
async def create_hotel(hotel_data: HotelSchema):
    async with async_session() as session:
        insert_hotel_stmt = insert(HotelModel).values(**hotel_data.model_dump())
        await session.execute(insert_hotel_stmt)
        await session.commit()
    return {'status': 'OK'}


@hotels_router.put('/{hotel_id}')
async def update_hotel(hotel_id: int, hotel_data: HotelSchema):
    hotel_to_update = get_hotel_to_update(hotel_id)
    hotel_to_update['title'] = hotel_data.title
    hotel_to_update['location'] = hotel_data.location
    return hotel_to_update


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
    hotel_to_update = get_hotel_to_update(hotel_id)
    hotel_to_update['title'] = hotel_data.title if hotel_data.title is not None else hotel_to_update['title']
    hotel_to_update['location'] = hotel_data.location if hotel_data.location is not None else hotel_to_update['location']
    return hotel_to_update


@hotels_router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}
