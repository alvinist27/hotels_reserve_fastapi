from pydantic import BaseModel, Field, field_validator

from src.utils.validation import check_not_only_whitespace


class HotelValidatorMixin:
    @field_validator('location', 'title')
    @staticmethod
    def check_not_only_whitespace(user_input: str):
        return check_not_only_whitespace(user_input)


class HotelAddSchema(BaseModel, HotelValidatorMixin):
    location: str = Field(description='Адрес отеля')
    title: str = Field(description='Название отеля')


class HotelSchema(HotelAddSchema):
    id: int


class HotelPatchSchema(BaseModel, HotelValidatorMixin):
    location: str | None = Field(default=None, description='Адрес отеля')
    title: str | None = Field(default=None, description='Название отеля')
