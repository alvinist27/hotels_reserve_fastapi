from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request, status
from pydantic import BaseModel

from src.services.auth import AuthService


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


PaginationDep = Annotated[Pagination, Depends()]
UserIDDep = Annotated[int, Depends(get_user_id)]
