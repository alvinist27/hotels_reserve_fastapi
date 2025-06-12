from pydantic import BaseModel, Field


class HotelSchema(BaseModel):
    name: str = Field(description='Название отеля'),
    title: str = Field(description='Название отеля на русском')


class HotelPatchSchema(BaseModel):
    name: str | None = Field(default=None, description='Название отеля')
    title: str | None = Field(default=None, description='Название отеля на русском')
