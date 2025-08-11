from src.models.facilities import FacilityORM
from src.repositories.base import BaseRepository
from src.schemas.facilities import FacilitySchema


class FacilityRepository(BaseRepository):
    model = FacilityORM
    schema = FacilitySchema
