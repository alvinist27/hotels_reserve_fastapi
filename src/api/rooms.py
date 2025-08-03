from fastapi import APIRouter, Body, Query, status

from src.database import async_session
from src.repositories.rooms import RoomRepository
from src.schemas.rooms import RoomAddSchema, RoomPatchSchema

rooms_router = APIRouter(prefix='/hotels', tags=['Rooms'])


@rooms_router.get('/{hotel_id}/rooms')
async def get_rooms(
    hotel_id: int,
    title: str | None = Query(None, description='Название комнаты'),
):
    async with async_session() as session:
        return await RoomRepository(session=session).get_all(
            hotel_id=hotel_id,
            title=title
        )


@rooms_router.get('/{hotel_id}/rooms/{room_id}')
async def get_room(hotel_id: int, room_id: int):
    async with async_session() as session:
        return await RoomRepository(session=session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@rooms_router.post('/{hotel_id}/rooms', status_code=status.HTTP_201_CREATED)
async def create_room(
    hotel_data: RoomAddSchema = Body(
        openapi_examples={
        '1': {
                'summary': 'Room example',
                'value': {
                    'hotel_id': 1,
                    'title': 'Super VIP',
                    'description': 'Оч хороший номер',
                    'price': 15000,
                    'quantity': 5,
                },
            },
        },
    ),
):
    async with async_session() as session:
        room = await RoomRepository(session).add(hotel_data)
        await session.commit()
    return {'status': 'OK', 'data': room}


@rooms_router.put('/{hotel_id}/rooms/{room_id}')
async def update_room(hotel_id: int, room_id: int, hotel_data: RoomAddSchema):
    async with async_session() as session:
        await RoomRepository(session).update(id=room_id, hotel_id=hotel_id, data=hotel_data)
        await session.commit()
    return {'status': 'OK'}


@rooms_router.patch('/{hotel_id}/rooms/{room_id}')
async def partial_update_room(
    hotel_id: int,
    room_id: int,
    hotel_data: RoomPatchSchema = Body(openapi_examples={
        '1': {
            'summary': 'Only title',
            'value': {
                'title': 'Super VIP',
            },
        },
        '2': {
            'summary': 'Only price',
            'value': {
                'price': '800000',
            },
        },
        '3': {
            'summary': 'Price and Title',
            'value': {
                'price': '777777',
                'title': 'President LUX',
            },
        },
    }),
):
    async with async_session() as session:
        await RoomRepository(session).update(id=room_id, hotel_id=hotel_id, exclude_unset=True, data=hotel_data)
        await session.commit()
    return {'status': 'OK'}


@rooms_router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_room(hotel_id: int, room_id: int):
    async with async_session() as session:
        await RoomRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {'status': 'OK'}
