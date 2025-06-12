from typing import Any

from fastapi import APIRouter, Body, HTTPException, Query

from schemas.hotels import HotelPatchSchema, HotelSchema

hotels_router = APIRouter(prefix='/hotels', tags=['Hotels'])

hotels = [
    {'id': 1, 'title': 'Sochi', 'name': 'sochi'},
    {'id': 2, 'title': 'Дубай', 'name': 'dubai'},
    {'id': 3, 'title': 'Мальдивы', 'name': 'maldivi'},
    {'id': 4, 'title': 'Геленджик', 'name': 'gelendzhik'},
    {'id': 5, 'title': 'Москва', 'name': 'moscow'},
    {'id': 6, 'title': 'Казань', 'name': 'kazan'},
    {'id': 7, 'title': 'Санкт-Петербург', 'name': 'spb'},
]


def get_hotel_to_update(hotel_id: int) -> dict[str, Any]:
    hotel_to_update = None
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel_to_update = hotel
    if not hotel_to_update:
        raise HTTPException(status_code=404, detail='Hotel not found')
    return hotel_to_update


@hotels_router.get('/')
def get_hotels(
    page: int = Query(1, description='Номер страницы', gt=0),
    per_page: int = Query(3, description='Отелей на странице', gt=0, lt=100),
    id: int | None = Query(None, description='ID отеля'),
    name: str | None = Query(None, description='Название отеля'),
    title: str | None = Query(None, description='Название отеля на русском'),
):
    filtered_hotels = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        if name and hotel['name'] != name:
            continue
        filtered_hotels.append(hotel)
    current_offset = (page-1) * per_page
    return {
        'page': page,
        'per_page': per_page,
        'total': len(filtered_hotels),
        'items': filtered_hotels[current_offset:current_offset+per_page]
    }


@hotels_router.post('/')
def create_hotel(hotel_data: HotelSchema):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': hotel_data.title,
        'name': hotel_data.name,
    })
    return {'status': 'OK'}


@hotels_router.put('/{hotel_id}')
def update_hotel(hotel_id: int, hotel_data: HotelSchema):
    hotel_to_update = get_hotel_to_update(hotel_id)
    hotel_to_update['title'] = hotel_data.title
    hotel_to_update['name'] = hotel_data.name
    return hotel_to_update


@hotels_router.patch('/{hotel_id}')
def partial_update_hotel(
    hotel_id: int,
    hotel_data: HotelPatchSchema = Body(openapi_examples={
        '1': {
            'summary': 'Only title',
            'value': {
                'title': 'Отель Сочи 5 звезд у моря',
            }
        },
        '2': {
            'summary': 'Only name',
            'value': {
                'name': 'dubai_fountain',
            }
        },
        '3': {
            'summary': 'Name and Title',
            'value': {
                'name': 'dubai_fountain',
                'title': 'dubai Сочи 5 звезд у моря',
            }
        }
    })
):
    hotel_to_update = get_hotel_to_update(hotel_id)
    hotel_to_update['title'] = hotel_data.title if hotel_data.title is not None else hotel_to_update['title']
    hotel_to_update['name'] = hotel_data.name if hotel_data.name is not None else hotel_to_update['name']
    return hotel_to_update


@hotels_router.delete('/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}
