from src.models.rooms import RoomORM
from src.repositories.base import BaseRepository
from src.schemas.rooms import RoomSchema


class RoomRepository(BaseRepository):
    model = RoomORM
    schema = RoomSchema
