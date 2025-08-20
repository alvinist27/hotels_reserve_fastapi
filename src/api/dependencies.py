from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request, status
from pydantic import BaseModel

from src.database import async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class Pagination(BaseModel):
    page: Annotated[int, Query(1, description='Номер страницы', ge=1)]
    per_page: Annotated[int, Query(3, description='Отелей на странице', ge=1, le=100)]


def get_token(request: Request) -> str:
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No token provided')
    return token


def get_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService.decode_access_token(token)
    return data['user_id']


def get_db_manager():
    return


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
PaginationDep = Annotated[Pagination, Depends()]
UserIDDep = Annotated[int, Depends(get_user_id)]
