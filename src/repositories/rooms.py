from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.models.rooms import RoomORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper, RoomWithRelsDataMapper
from src.repositories.utils import get_rooms_ids_for_booking
from src.schemas.rooms import RoomSchema


class RoomRepository(BaseRepository):
    model = RoomORM
    mapper = RoomDataMapper

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = get_rooms_ids_for_booking(date_from, date_to, hotel_id)
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .where(self.model.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomWithRelsDataMapper.map_to_domain_entity(model) for model in result.unique().scalars().all()]

    async def get_one_or_none(self, **filter_by) -> RoomSchema | None:
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        row = result.unique().scalars().one_or_none()
        return None if row is None else RoomWithRelsDataMapper.map_to_domain_entity(row)
