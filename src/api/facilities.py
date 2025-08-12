from fastapi import APIRouter, status

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAddSchema, FacilitySchema

facilities_router = APIRouter(prefix='/facilities', tags=['Facilities'])


@facilities_router.get('/')
async def get_facilities(db: DBDep) -> list[FacilitySchema]:
    return await db.facilities.get_all()


@facilities_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_facility(
    db: DBDep,
    facility_data: FacilityAddSchema,
) -> dict:
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {'status': 'OK', 'data': facility}
