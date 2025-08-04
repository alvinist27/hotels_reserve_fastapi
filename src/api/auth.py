from fastapi import APIRouter, HTTPException, Response, status

from src.api.dependencies import DBDep, UserIDDep
from src.schemas.users import UserAddRequestSchema
from src.services.auth import AuthService

auth_router = APIRouter(prefix='/auth', tags=['Authorization'])


@auth_router.post('/login', status_code=status.HTTP_201_CREATED)
async def login(db: DBDep, user_data: UserAddRequestSchema, response: Response):
    user = await db.users.get_user_with_password(email=user_data.email)
    if not (user and AuthService().verify_password(user_data.password, user.password)):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Auth data error')
    access_token = AuthService.encode_access_token({'user_id': user.id})
    response.set_cookie('access_token', access_token)
    return {'access_token': access_token}


@auth_router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(db: DBDep, user_data: UserAddRequestSchema):
    user_data.password = AuthService().hash_password(user_data.password)
    await db.users.add(user_data)
    await db.commit()
    return {'status': 'OK'}


@auth_router.get('/me', status_code=status.HTTP_201_CREATED)
async def get_user_info(user_id: UserIDDep):
    return {'user_id': user_id}


@auth_router.post('/logout', status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response, _: UserIDDep):
    response.delete_cookie('access_token')
