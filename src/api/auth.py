from fastapi import APIRouter, HTTPException, Response, status

from src.api.dependencies import UserIDDep
from src.database import async_session
from src.repositories.users import UserRepository
from src.schemas.users import UserAddRequestSchema
from src.services.auth import AuthService

auth_router = APIRouter(prefix='/auth', tags=['Authorization'])


@auth_router.post('/login', status_code=status.HTTP_201_CREATED)
async def login(user_data: UserAddRequestSchema, response: Response):
    async with async_session() as session:
        user = await UserRepository(session).get_user_with_password(email=user_data.email)
        if not (user and AuthService().verify_password(user_data.password, user.password)):
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Auth data error')
        access_token = AuthService.encode_access_token({'user_id': user.id})
        response.set_cookie('access_token', access_token)
    return {'access_token': access_token}


@auth_router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user_data: UserAddRequestSchema):
    user_data.password = AuthService().hash_password(user_data.password)
    async with async_session() as session:
        await UserRepository(session).add(user_data)
        await session.commit()
    return {'status': 'OK'}


@auth_router.get('/me', status_code=status.HTTP_201_CREATED)
async def get_user_info(user_id: UserIDDep):
    return {'user_id': user_id}


@auth_router.post('/logout', status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response, _: UserIDDep):
    response.delete_cookie('access_token')
