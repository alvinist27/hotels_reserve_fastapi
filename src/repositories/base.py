import logging

from asyncpg.exceptions import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.database import Base
from src.exceptions import InputDataException, ObjectAlreadyExistsException, ObjectNotFoundException
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model: Base = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter_values, **filter_by) -> list[BaseModel]:
        query = (
            select(self.model)
            .filter(*filter_values)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(row) for row in result.scalars().all()]

    async def get_all(self, *args, **kwargs) -> list[BaseModel]:
        return await self.get_filtered()

    async def get_one(self, **filter_by) -> BaseModel:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(model)

    async def get_one_or_none(self, **filter_by) -> BaseModel | None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        row = result.scalars().one_or_none()
        return None if row is None else self.mapper.map_to_domain_entity(row)

    async def add(self, data: BaseModel) -> BaseModel:
        insert_statement = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            insert_result = await self.session.execute(insert_statement)
            row = insert_result.scalars().one()
        except IntegrityError as exception:
            logging.error(f'IntegrityError while add! data:{data} type: {exception.orig.__cause__} exc: {exception}')
            if isinstance(exception.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from exception
            raise exception
        return self.mapper.map_to_domain_entity(row)

    async def add_bulk(self, add_data: list[BaseModel]) -> None:
        insert_statement = insert(self.model).values([item.model_dump() for item in add_data])
        try:
            await self.session.execute(insert_statement)
        except IntegrityError as exception:
            raise ObjectNotFoundException from exception

    async def update(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset, exclude_none=exclude_unset))
        )
        try:
            await self.session.execute(update_stmt)
        except IntegrityError as exception:
            raise InputDataException from exception

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
