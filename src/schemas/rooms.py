from pydantic import BaseModel, Field

from src.schemas.facilities import FacilitySchema


class RoomPatchRequestSchema(BaseModel):
    title: str | None = Field(default=None, description='Название комнаты')
    description: str | None = Field(default=None, description='Описание комнаты')
    price: int | None = Field(default=None, description='Цена комнаты')
    quantity: int | None = Field(default=None, description='Количество комнат')
    facility_ids: list[int] | None = Field(default=None, description='ID удобства')


class RoomPatchSchema(BaseModel):
    hotel_id: int | None = Field(default=None, description='ID отеля')
    title: str | None = Field(default=None, description='Название комнаты')
    description: str | None = Field(default=None, description='Описание комнаты')
    price: int | None = Field(default=None, description='Цена комнаты')
    quantity: int | None = Field(default=None, description='Количество комнат')


class RoomAddRequestSchema(BaseModel):
    title: str = Field(description='Название комнаты')
    description: str = Field(default='', description='Описание комнаты')
    price: int = Field(description='Цена комнаты')
    quantity: int = Field(description='Количество комнат')
    facility_ids: list[int] | None = Field(description='ID удобства', default=None)


class RoomAddSchema(BaseModel):
    hotel_id: int = Field(description='ID отеля')
    title: str = Field(description='Название комнаты')
    description: str = Field(default='', description='Описание комнаты')
    price: int = Field(description='Цена комнаты')
    quantity: int = Field(description='Количество комнат')


class RoomSchema(RoomAddSchema):
    id: int


class RoomWithRels(RoomSchema):
    facilities: list[FacilitySchema]
