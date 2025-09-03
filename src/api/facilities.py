from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exceptions import FacilityAlreadyExistsException, FacilityAlreadyExistsHTTPException
from src.schemas.facilities import FacilityAddSchema
from src.services.facilities import FacilityService

facilities_router = APIRouter(prefix='/facilities', tags=['Facilities'])


@facilities_router.get('')
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_facilities()


@facilities_router.post('')
async def create_facility(db: DBDep, facility_data: FacilityAddSchema = Body()):
    try:
        facility = await FacilityService(db).create_facility(facility_data)
    except FacilityAlreadyExistsException:
        raise FacilityAlreadyExistsHTTPException
    return {'status': 'OK', 'data': facility}
