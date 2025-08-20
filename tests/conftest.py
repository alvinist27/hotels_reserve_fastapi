import json

import pytest

from httpx import AsyncClient, ASGITransport
from src.config import settings
from src.database import Base, engine_null_pool
from src.main import app
from src.models import *


@pytest.fixture(scope='session', autouse=True)
def check_settings_mode():
    assert settings.MODE == 'TEST'


@pytest.fixture(scope='session', autouse=True)
async def setup_database(check_settings_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='session', autouse=True)
async def create_hotels(setup_database):
    with open('tests/fixtures/mock_hotels.json') as file:
        file_data = file.read()
    hotels_data = json.loads(file_data)
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        for hotel_data in hotels_data:
            await ac.post('/hotels/', json=hotel_data)


@pytest.fixture(scope='session', autouse=True)
async def create_rooms(setup_database):
    with open('tests/fixtures/mock_rooms.json') as file:
        file_data = file.read()
    rooms_data = json.loads(file_data)
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        for room_data in rooms_data:
            hotel_id = room_data.pop('hotel_id')
            await ac.post(f'hotels/{hotel_id}/rooms', json=room_data)


@pytest.fixture(scope='session', autouse=True)
async def register_user(setup_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        await ac.post(
            '/auth/register',
            json={
                'email': 'kot@pes.com',
                'password': '1234',
            },
        )
