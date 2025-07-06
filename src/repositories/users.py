from src.models.users import UserORM
from src.repositories.base import BaseRepository
from src.schemas.users import UserSchema


class UserRepository(BaseRepository):
    model = UserORM
    schema = UserSchema
