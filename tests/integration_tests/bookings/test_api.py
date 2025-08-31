import pytest

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize('room_id, date_from, date_to, status_code', [
    (1, '2024-08-01', '2024-08-10', 200),
    (1, '2024-08-02', '2024-08-11', 200),
    (1, '2024-08-03', '2024-08-12', 200),
    (1, '2024-08-04', '2024-08-13', 200),
    (1, '2024-08-05', '2024-08-14', 200),
    (1, '2024-08-06', '2024-08-15', 400),
    (1, '2024-08-17', '2024-08-25', 200),
])
async def test_add_booking(
    room_id,
    date_from,
    date_to,
    status_code,
    db,
    authenticated_ac
):
    response = await authenticated_ac.post(
        '/bookings/',
        json={
            'room_id': room_id,
            'date_from': date_from,
            'date_to': date_to,
        }
    )
    assert response.status_code == status_code
    if response.status_code != 200:
        return
    res = response.json()
    assert isinstance(res, dict)
    assert res['status'] == 'OK'
    assert 'data' in res


@pytest.fixture(scope='module')
async def delete_bookings():
    async for db_ in get_db_null_pool():
        await db_.bookings.delete()
        await db_.commit()


@pytest.mark.parametrize('room_id, date_from, date_to, booking_count', [
    (1, '2024-08-01', '2024-08-10', 1),
    (1, '2024-08-02', '2024-08-11', 2),
    (1, '2024-08-03', '2024-08-12', 3),
])
async def test_my_bookings(
    room_id,
    date_from,
    date_to,
    booking_count,
    authenticated_ac,
    delete_bookings,
):
    response = await authenticated_ac.post(
        '/bookings/',
        json={
            'room_id': room_id,
            'date_from': date_from,
            'date_to': date_to,
        }
    )
    assert response.status_code == 200
    response = await authenticated_ac.get('/bookings/me')
    assert len(response.json()) == booking_count
