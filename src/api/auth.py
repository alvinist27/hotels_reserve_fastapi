from fastapi import APIRouter, Response

from src.api.dependencies import DBDep, UserIDDep
from src.exceptions import (
    EmailNotRegisteredException,
    EmailNotRegisteredHTTPException,
    IncorrectPasswordException,
    IncorrectPasswordHTTPException,
    UserAlreadyExistsException,
    UserEmailAlreadyExistsHTTPException,
)
from src.schemas.users import UserAddRequestSchema
from src.services.auth import AuthService

auth_router = APIRouter(prefix='/auth', tags=['Auth'])


@auth_router.post('/register')
async def register_user(data: UserAddRequestSchema, db: DBDep):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    return {'status': 'OK'}


@auth_router.post('/login')
async def login_user(
    data: UserAddRequestSchema,
    response: Response,
    db: DBDep,
):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException

    response.set_cookie('access_token', access_token)
    return {'access_token': access_token}


@auth_router.get('/me')
async def get_me(
    user_id: UserIDDep,
    db: DBDep,
):
    return await AuthService(db).get_one_or_none_user(user_id)


@auth_router.post('/logout')
async def logout(response: Response):
    response.delete_cookie('access_token')
    return {'status': 'OK'}
