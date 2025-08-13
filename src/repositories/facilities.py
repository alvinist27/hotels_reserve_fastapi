from src.models.facilities import FacilityORM, RoomFacilityORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilityDataMapper
from src.schemas.facilities import FacilitySchema, RoomFacilitySchema
from sqlalchemy import select, delete


class FacilityRepository(BaseRepository):
    model = FacilityORM
    mapper = FacilityDataMapper


class RoomFacilityRepository(BaseRepository):
    model = RoomFacilityORM
    mapper = FacilityDataMapper

    async def update_bulk(self, data: list[id], **filter_by) -> None:
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
