from pydantic import BaseModel, Field
from datetime import date


class BookingRequestAddSchema(BaseModel):
    date_from: date = Field(description='Дата заезда')
    date_to: date = Field(description='Дата выезда')
    price: int = Field(description='Цена бронирования')
    room_id: int = Field(description='ID комнаты')


class BookingAddSchema(BookingRequestAddSchema):
    user_id: int = Field(description='ID пользователя')


class BookingSchema(BookingAddSchema):
    id: int = Field(description='ID бронирования')
