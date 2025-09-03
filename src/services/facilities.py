from src.exceptions import FacilityAlreadyExistsException, ObjectAlreadyExistsException
from src.schemas.facilities import FacilityAddSchema
from src.services.base import BaseService


class FacilityService(BaseService):
    async def create_facility(self, data: FacilityAddSchema):
        try:
            facility = await self.db.facilities.add(data)
            await self.db.commit()
        except ObjectAlreadyExistsException:
            raise FacilityAlreadyExistsException
        return facility

    async def get_facilities(self):
        return await self.db.facilities.get_all()
