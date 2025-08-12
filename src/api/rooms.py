from fastapi import APIRouter, Body, status, Query
from datetime import date
from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilitySchema
from src.schemas.rooms import RoomAddRequestSchema, RoomAddSchema, RoomPatchRequestSchema, RoomPatchSchema

rooms_router = APIRouter(prefix='/hotels', tags=['Rooms'])


@rooms_router.get('/{hotel_id}/rooms')
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example='2024-08-05'),
    date_to: date = Query(example='2024-08-08'),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@rooms_router.get('/{hotel_id}/rooms/{room_id}')
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@rooms_router.post('/{hotel_id}/rooms', status_code=status.HTTP_201_CREATED)
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequestSchema = Body(
        openapi_examples={
        '1': {
                'summary': 'Room example',
                'value': {
                    'title': 'Super VIP',
                    'description': 'Оч хороший номер',
                    'price': 15000,
                    'quantity': 5,
                    'facility_ids': [1],
                },
            },
        },
    ),
):
    create_data = RoomAddSchema(**room_data.model_dump(), hotel_id=hotel_id)
    room = await db.rooms.add(create_data)
    await db.rooms_facilities.add_bulk([
        RoomFacilitySchema(room_id=room.id, facility_id=facility_id) for facility_id in room_data.facility_ids
    ])
    await db.commit()
    return {'status': 'OK', 'data': room}


@rooms_router.put('/{hotel_id}/rooms/{room_id}')
async def update_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequestSchema):
    update_data = RoomAddSchema(**room_data.model_dump(), hotel_id=hotel_id)
    await db.rooms.update(id=room_id, hotel_id=hotel_id, data=update_data)
    await db.rooms_facilities.update_bulk(
        room_data.facility_ids,
        room_id=room_id,
    )
    await db.commit()
    return {'status': 'OK'}


@rooms_router.patch('/{hotel_id}/rooms/{room_id}')
async def partial_update_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequestSchema = Body(openapi_examples={
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
        '4': {
            'summary': 'facilities',
            'value': {
                'facility_ids': [1],
            },
        },
    }),
):
    update_data = RoomPatchSchema(**room_data.model_dump(), hotel_id=hotel_id)
    await db.rooms.update(id=room_id, hotel_id=hotel_id, exclude_unset=True, data=update_data)
    if room_data.facility_ids is not None:
        await db.rooms_facilities.update_bulk(
            room_data.facility_ids,
            room_id=room_id,
        )
    await db.commit()
    return {'status': 'OK'}


@rooms_router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {'status': 'OK'}
