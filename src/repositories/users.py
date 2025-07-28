from pydantic import BaseModel, EmailStr
from sqlalchemy import select

from src.models.users import UserORM
from src.repositories.base import BaseRepository
from src.schemas.users import UserSchema, UserWithPasswordSchema


class UserRepository(BaseRepository):
    model = UserORM
    schema = UserSchema

    async def get_user_with_password(self, email: EmailStr) -> BaseModel | None:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        row = result.scalars().one_or_none()
        return UserWithPasswordSchema.model_validate(row, from_attributes=True)
