from src.models.rooms import RoomORM
from src.repositories.base import BaseRepository


class RoomRepository(BaseRepository):
    model = RoomORM
