import pytest
from httpx import AsyncClient


async def test_get_hotels(ac):
    response = await ac.get(
        '/hotels',
        params={
            'date_from': '2024-08-01',
            'date_to': '2024-08-10',
        }
    )
    assert response.status_code == 200


@pytest.fixture
async def hotel_id(ac: AsyncClient):
    response = await ac.post('/hotels', json={'title': 'Test Hotel', 'location': 'Test Location'})
    if response.status_code == 200:
        return response.json()['data']['id']
    return None

async def test_cannot_create_duplicate_hotels(ac: AsyncClient):
    hotel_data = {'title': 'Duplicate Hotel', 'location': 'Same Location'}
    response1 = await ac.post('/hotels', json=hotel_data)
    response2 = await ac.post('/hotels', json=hotel_data)
    assert response1.status_code == 200
    assert response2.status_code == 409

async def test_cannot_create_hotel_empty_title(ac: AsyncClient):
    response = await ac.post('/hotels', json={'title': '', 'location': 'Test Location'})
    assert response.status_code == 422

async def test_cannot_create_hotel_empty_location(ac: AsyncClient):
    response = await ac.post('/hotels', json={'title': 'Test Hotel', 'location': ''})
    assert response.status_code == 422

async def test_put_works_correctly(ac: AsyncClient, hotel_id):
    response = await ac.put(f'/hotels/{hotel_id}', json={'title': 'Updated', 'location': 'Updated'})
    assert response.status_code == 200

async def test_patch_works_correctly(ac: AsyncClient, hotel_id):
    response = await ac.patch(f'/hotels/{hotel_id}', json={'title': 'Patched'})
    assert response.status_code == 200

async def test_cannot_delete_same_hotel_twice(ac: AsyncClient, hotel_id):
    response1 = await ac.delete(f'/hotels/{hotel_id}')
    response2 = await ac.delete(f'/hotels/{hotel_id}')
    assert response1.status_code == 200
    assert response2.status_code == 404

async def test_put_empty_title_returns_400(ac: AsyncClient, hotel_id):
    response = await ac.put(f'/hotels/{hotel_id}', json={'title': '', 'location': 'Test'})
    assert response.status_code == 422
    response = await ac.put(f'/hotels/{hotel_id}', json={'title': 'Test', 'location': ''})
    assert response.status_code == 422
