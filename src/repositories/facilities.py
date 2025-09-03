from collections.abc import Sequence

from sqlalchemy import delete, insert, select

from src.models.facilities import FacilityORM, RoomFacilityORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilityDataMapper, RoomFacilityDataMapper
from src.schemas.facilities import RoomFacilitySchema


class FacilityRepository(BaseRepository):
    model = FacilityORM
    mapper = FacilityDataMapper


class RoomFacilityRepository(BaseRepository):
    model = RoomFacilityORM
    mapper = RoomFacilityDataMapper

    async def update_bulk(self, data: list[int], **filter_by) -> None:
        room_id = filter_by.get('room_id')
        facility_ids_query = (
            select(self.model.facility_id)
            .select_from(self.model)
            .filter_by(room_id=room_id)
        )
        result = await self.session.execute(facility_ids_query)
        facility_ids = result.scalars().all()
        facility_to_create = set(data) - set(facility_ids)
        if facility_to_create:
            await self.add_bulk([RoomFacilitySchema(facility_id=id, room_id=room_id) for id in facility_to_create])
        facility_to_delete = list(set(facility_ids) - set(data))
        if facility_to_delete:
            await self.delete_bulk(facility_to_delete, room_id=room_id)

    async def delete_bulk(self, ids: list[id], room_id: int) -> None:
        delete_stmt = delete(self.model).where(self.model.facility_id.in_(ids)).filter_by(room_id=room_id)
        await self.session.execute(delete_stmt)

    async def set_room_facilities(self, room_id: int, facilities_ids: list[int]) -> None:
        get_current_facilities_ids_query = select(self.model.facility_id).filter_by(room_id=room_id)
        res = await self.session.execute(get_current_facilities_ids_query)
        current_facilities_ids: Sequence[int] = res.scalars().all()
        ids_to_delete: list[int] = list(set(current_facilities_ids) - set(facilities_ids))
        ids_to_insert: list[int] = list(set(facilities_ids) - set(current_facilities_ids))

        if ids_to_delete:
            delete_m2m_facilities_stmt = delete(self.model).filter(  # type: ignore
                self.model.room_id == room_id,  # type: ignore
                self.model.facility_id.in_(ids_to_delete),  # type: ignore
            )
            await self.session.execute(delete_m2m_facilities_stmt)

        if ids_to_insert:
            insert_m2m_facilities_stmt = insert(self.model).values(  # type: ignore
                [{'room_id': room_id, 'facility_id': f_id} for f_id in ids_to_insert]
            )
            await self.session.execute(insert_m2m_facilities_stmt)
