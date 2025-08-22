async def test_get_facilities(ac):
    response = await ac.get('/facilities/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_create_facilities(ac):
    facility_title = '123'
    response = await ac.post('/facilities/', json={'title': facility_title})
    assert response.status_code == 201
    res = response.json()
    assert isinstance(res, dict)
    assert 'data' in res
    assert res['data']['title'] == facility_title
