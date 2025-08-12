from pydantic import BaseModel, Field


class FacilityAddSchema(BaseModel):
    title: str = Field(description='Название удобства')


class FacilitySchema(FacilityAddSchema):
    id: int


class RoomFacilitySchema(BaseModel):
    facility_id: int
    room_id: int
