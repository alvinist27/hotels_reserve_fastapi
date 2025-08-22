import json

import pytest
from httpx import ASGITransport, AsyncClient

from src.config import settings
from src.database import async_session_maker_null_pool, Base, engine_null_pool
from src.main import app
from src.schemas.hotels import HotelAddSchema
from src.schemas.rooms import RoomAddSchema
from src.utils.db_manager import DBManager


@pytest.fixture(scope='session', autouse=True)
def check_settings_mode():
    assert settings.MODE == 'TEST'


@pytest.fixture(scope='function')
async def db() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope='session')
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='session', autouse=True)
async def setup_database(check_settings_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open('tests/fixtures/mock_hotels.json', encoding='utf-8') as file:
        hotels_data = json.load(file)
    with open('tests/fixtures/mock_rooms.json', encoding='utf-8') as file:
        rooms_data = json.load(file)
    hotels = [HotelAddSchema.model_validate(hotel, from_attributes=True) for hotel in hotels_data]
    rooms = [RoomAddSchema.model_validate(room, from_attributes=True) for room in rooms_data]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest.fixture(scope='session', autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
        '/auth/register',
        json={
            'email': 'kot@pes.com',
            'password': '1234',
        },
    )
