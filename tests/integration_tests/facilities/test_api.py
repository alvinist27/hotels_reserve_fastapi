async def test_get_facilities(ac):
    response = await ac.get('/facilities/')
    assert response.status_code == 200


async def test_create_facilities(ac):
    response = await ac.post('/facilities/', json={'title': '123'})
    assert response.status_code == 201
