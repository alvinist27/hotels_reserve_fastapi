from sqlalchemy import select

from src.models.hotels import HotelORM
from src.repositories.base import BaseRepository


class HotelRepository(BaseRepository):
    model = HotelORM

    async def get_all(self, location, title, limit, offset):
        query = select(self.model)
        if location:
            query = query.filter(self.model.location.icontains(location.strip()))
        if title:
            query = query.filter(self.model.title.icontains(title.strip()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
