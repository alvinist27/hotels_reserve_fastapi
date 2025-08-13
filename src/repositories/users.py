from pydantic import BaseModel, EmailStr
from sqlalchemy import select

from src.models.users import UserORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas.users import UserWithPasswordSchema


class UserRepository(BaseRepository):
    model = UserORM
    mapper = UserDataMapper

    async def get_user_with_password(self, email: EmailStr) -> BaseModel | None:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        row = result.scalars().one_or_none()
        return UserWithPasswordSchema.model_validate(row, from_attributes=True)
