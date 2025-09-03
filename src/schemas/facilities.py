from pydantic import BaseModel, Field, field_validator

from src.utils.validation import check_not_only_whitespace


class FacilityValidatorMixin:
    @field_validator('title')
    @staticmethod
    def check_not_only_whitespace(user_input: str):
        return check_not_only_whitespace(user_input)


class FacilityAddSchema(BaseModel, FacilityValidatorMixin):
    title: str = Field(description='Название удобства')


class FacilitySchema(FacilityAddSchema):
    id: int


class RoomFacilitySchema(BaseModel):
    facility_id: int
    room_id: int
