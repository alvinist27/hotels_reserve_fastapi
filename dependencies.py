from typing import Annotated

from fastapi import Query, Depends
from pydantic import BaseModel


class Pagination(BaseModel):
    page: Annotated[int, Query(1, description='Номер страницы', ge=1)]
    per_page: Annotated[int, Query(3, description='Отелей на странице', ge=1, le=100)]


PaginationDep = Annotated[Pagination, Depends()]
