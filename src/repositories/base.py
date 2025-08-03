from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update

from src.database import Base


class BaseRepository:
    model: Base = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, **filter_by) -> list[BaseModel]:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.schema.model_validate(row, from_attributes=True) for row in result.scalars().all()]

    async def get_all(self, *args, **kwargs) -> list[BaseModel]:
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by) -> BaseModel | None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        row = result.scalars().one_or_none()
        return None if row is None else self.schema.model_validate(row, from_attributes=True)

    async def add(self, data: BaseModel) -> BaseModel:
        insert_statement = insert(self.model).values(**data.model_dump()).returning(self.model)
        insert_result = await self.session.execute(insert_statement)
        row = insert_result.scalars().one()
        return self.schema.model_validate(row, from_attributes=True)

    async def update(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
