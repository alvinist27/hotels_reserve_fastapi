from pydantic import BaseModel, Field


class HotelSchema(BaseModel):
    location: str = Field(description='Адрес отеля'),
    title: str = Field(description='Название отеля')


class HotelPatchSchema(BaseModel):
    location: str | None = Field(default=None, description='Адрес отеля')
    title: str | None = Field(default=None, description='Название отеля')
