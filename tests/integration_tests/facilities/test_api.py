from httpx import AsyncClient


async def test_get_facilities(ac):
    response = await ac.get('/facilities')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

async def test_create_facilities(ac):
    facility_title = '123'
    response = await ac.post('/facilities', json={'title': facility_title})
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert 'data' in res
    assert res['data']['title'] == facility_title

async def test_cannot_create_duplicate_facilities(ac: AsyncClient):
    facility_data = {'title': 'Wi-Fi'}
    response1 = await ac.post('/facilities', json=facility_data)
    response2 = await ac.post('/facilities', json=facility_data)
    assert response1.status_code == 200
    assert response2.status_code == 409

async def test_can_create_facility_with_empty_name(ac: AsyncClient):
    response = await ac.post('/facilities', json={'title': ''})
    assert response.status_code == 422

async def test_can_create_facility_with_whitespace_name(ac: AsyncClient):
    response = await ac.post('/facilities', json={'title': '   '})
    assert response.status_code == 422

async def test_create_multiple_different_facilities(ac: AsyncClient):
    response1 = await ac.post('/facilities', json={'title': 'Pool'})
    response2 = await ac.post('/facilities', json={'title': 'Spa'})
    response3 = await ac.post('/facilities', json={'title': 'Gym'})
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200
