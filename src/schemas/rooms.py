from pydantic import BaseModel, Field


class RoomPatchRequestSchema(BaseModel):
    title: str | None = Field(default=None, description='Название комнаты')
    description: str | None = Field(default=None, description='Описание комнаты')
    price: int | None = Field(default=None, description='Цена комнаты')
    quantity: int | None = Field(default=None, description='Количество комнат')


class RoomPatchSchema(RoomPatchRequestSchema):
    hotel_id: int | None = Field(default=None, description='ID отеля')


class RoomAddRequestSchema(BaseModel):
    title: str = Field(description='Название комнаты')
    description: str = Field(default='', description='Описание комнаты')
    price: int = Field(description='Цена комнаты')
    quantity: int = Field(description='Количество комнат')


class RoomAddSchema(RoomAddRequestSchema):
    hotel_id: int = Field(description='ID отеля')


class RoomSchema(RoomAddSchema):
    id: int
