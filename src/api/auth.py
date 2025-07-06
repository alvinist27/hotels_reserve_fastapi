from fastapi import APIRouter, Body, Query, status

from passlib.context import CryptContext

from src.database import async_session
from src.repositories.users import UserRepository
from src.schemas.users import UserAddRequestSchema

auth_router = APIRouter(prefix='/auth', tags=['Authorization'])
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@auth_router.post('/', status_code=status.HTTP_201_CREATED)
async def register(user_data: UserAddRequestSchema):
    user_data.password = pwd_context.hash(user_data.password)
    async with async_session() as session:
        await UserRepository(session).add(user_data)
        await session.commit()
    return {'status': 'OK'}
