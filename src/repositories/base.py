from pydantic import BaseModel
from sqlalchemy import and_, delete, insert, select, update


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        insert_statement = insert(self.model).values(**data.model_dump()).returning(self.model)
        insert_result = await self.session.execute(insert_statement)
        return insert_result.scalars().one()

    async def update(self, data: BaseModel, **filter_by) -> None:
        conditions = [getattr(self.model, key) == value for key, value in filter_by.items()]
        update_stmt = update(self.model).where(and_(*conditions)).values(**data.model_dump())
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        conditions = [getattr(self.model, key) == value for key, value in filter_by.items()]
        delete_stmt = delete(self.model).where(and_(*conditions))
        await self.session.execute(delete_stmt)
