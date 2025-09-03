from pydantic import BaseModel, Field, field_validator

from src.schemas.facilities import FacilitySchema
from src.utils.validation import check_not_only_whitespace


class RoomValidatorMixin:
    @field_validator('title')
    @staticmethod
    def check_not_only_whitespace(user_input: str):
        return check_not_only_whitespace(user_input)


class RoomPatchRequestSchema(BaseModel, RoomValidatorMixin):
    title: str | None = Field(default=None, description='Название комнаты')
    description: str | None = Field(default=None, description='Описание комнаты')
    price: int | None = Field(default=None, description='Цена комнаты')
    quantity: int | None = Field(default=None, description='Количество комнат')
    facility_ids: list[int] | None = Field(default=None, description='ID удобства')


class RoomPatchSchema(BaseModel, RoomValidatorMixin):
    hotel_id: int | None = Field(default=None, description='ID отеля')
    title: str | None = Field(default=None, description='Название комнаты')
    description: str | None = Field(default=None, description='Описание комнаты')
    price: int | None = Field(default=None, description='Цена комнаты')
    quantity: int | None = Field(default=None, description='Количество комнат')


class RoomAddRequestSchema(BaseModel, RoomValidatorMixin):
    title: str = Field(description='Название комнаты')
    description: str = Field(default='', description='Описание комнаты')
    price: int = Field(description='Цена комнаты')
    quantity: int = Field(description='Количество комнат')
    facility_ids: list[int] | None = Field(description='ID удобства', default=None)


class RoomAddSchema(BaseModel, RoomValidatorMixin):
    hotel_id: int = Field(description='ID отеля')
    title: str = Field(description='Название комнаты')
    description: str = Field(default='', description='Описание комнаты')
    price: int = Field(description='Цена комнаты')
    quantity: int = Field(description='Количество комнат')


class RoomSchema(RoomAddSchema):
    id: int


class RoomWithRels(RoomSchema):
    facilities: list[FacilitySchema]
