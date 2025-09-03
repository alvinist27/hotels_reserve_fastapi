from httpx import AsyncClient


async def test_cannot_get_rooms_nonexistent_hotel(ac: AsyncClient):
    response = await ac.get('1/rooms/999999')
    assert response.status_code == 404


async def test_create_room_works_correctly(ac: AsyncClient):
    hotel_response = await ac.post('/hotels', json={'title': 'Test Hotel1', 'location': 'Test Location1'})
    hotel_id = hotel_response.json()['data']['id']

    room_data = {
        'hotel_id': hotel_id,
        'title': 'Standard Room',
        'price': 100,
        'quantity': 5
    }

    response = await ac.post(f'hotels/{hotel_id}/rooms', json=room_data)
    assert response.status_code == 200


async def test_cannot_create_room_nonexistent_hotel(ac: AsyncClient):
    room_data = {
        'hotel_id': 999999,
        'title': 'Standard Room',
        'price': 100,
        'quantity': 5
    }

    response = await ac.post(f'/hotels/{999999}/rooms', json=room_data)
    assert response.status_code == 404


async def test_cannot_create_room_empty_title(ac: AsyncClient):
    hotel_response = await ac.post('/hotels', json={'title': 'Test Hotel2', 'location': 'Test Location'})
    hotel_id = hotel_response.json()['data']['id']

    room_data = {
        'hotel_id': hotel_id,
        'title': '',
        'price': 100,
        'quantity': 5
    }

    response = await ac.post('/hotels/{hotel_id}/rooms', json=room_data)
    assert response.status_code == 422


async def test_cannot_create_room_invalid_price(ac: AsyncClient):
    hotel_response = await ac.post('/hotels', json={'title': 'Test Hotel3', 'location': 'Test Location'})
    hotel_id = hotel_response.json()['data']['id']

    room_data = {
        'hotel_id': hotel_id,
        'title': 'Standard Room',
        'price': -100,
        'quantity': 5
    }

    response = await ac.post('/hotels/{hotel_id}/rooms', json=room_data)
    assert response.status_code == 422


async def test_cannot_create_room_invalid_quantity(ac: AsyncClient):
    hotel_response = await ac.post('/hotels', json={'title': 'Test Hotel4', 'location': 'Test Location'})
    hotel_id = hotel_response.json()['data']['id']

    room_data = {
        'hotel_id': hotel_id,
        'title': 'Standard Room',
        'price': 100,
        'quantity': -5
    }

    response = await ac.post('/hotels/{hotel_id}/rooms', json=room_data)
    assert response.status_code == 422
