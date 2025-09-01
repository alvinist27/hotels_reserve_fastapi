from src.schemas.facilities import FacilityAddSchema
from src.services.base import BaseService


class FacilityService(BaseService):
    async def create_facility(self, data: FacilityAddSchema):
        facility = await self.db.facilities.add(data)
        await self.db.commit()
        return facility

    async def get_facilities(self):
        return await self.db.facilities.get_all()
