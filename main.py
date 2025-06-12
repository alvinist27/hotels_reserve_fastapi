from typing import Any

import uvicorn
from fastapi import Body, FastAPI, Query, HTTPException

app = FastAPI()

hotels = [
    {'id': 1, 'title': 'Sochi', 'name': 'Сочи'},
    {'id': 2, 'title': 'Dubai', 'name': 'Дубай'},
]


def get_hotel_to_update(hotel_id: int) -> dict[str, Any]:
    hotel_to_update = None
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel_to_update = hotel
    if not hotel_to_update:
        raise HTTPException(status_code=404, detail='Hotel not found')
    return hotel_to_update


@app.get('/hotels')
def get_hotels(
    id: int | None = Query(None, description='ID отеля'),
    title: str | None = Query(None, description='Название отеля'),
    name: str | None = Query(None, description='Название отеля на русском'),
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
    return filtered_hotels


@app.post('/hotels')
def create_hotel(
    title: str = Body(embed=True),
    name: str = Body(embed=True),
):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': title,
        'name': name,
    })
    return {'status': 'OK'}


@app.put('/hotels/{hotel_id}')
def update_hotel(
    hotel_id: int,
    title: str = Body(description='Название отеля'),
    name: str = Body(description='Название отеля на русском'),
):
    hotel_to_update = get_hotel_to_update(hotel_id)
    hotel_to_update['title'] = title
    hotel_to_update['name'] = name
    return hotel_to_update


@app.patch('/hotels/{hotel_id}')
def partial_update_hotel(
    hotel_id: int,
    title: str | None = Body(None, description='Название отеля'),
    name: str | None = Body(None, description='Название отеля на русском'),
):
    hotel_to_update = get_hotel_to_update(hotel_id)
    hotel_to_update['title'] = title if title is not None else hotel_to_update['title']
    hotel_to_update['name'] = name if name is not None else hotel_to_update['name']
    return hotel_to_update


@app.delete('/hotels/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
