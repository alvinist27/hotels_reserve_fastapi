from pydantic import BaseModel, EmailStr, Field


class UserAddRequestSchema(BaseModel):
    email: EmailStr = Field(description='E-mail пользователя')
    password: str = Field(description='Пароль пользователя', min_length=6)


class UserSchema(BaseModel):
    id: int
    email: EmailStr = Field(description='E-mail пользователя')


class UserWithPasswordSchema(UserSchema):
    password: str = Field(description='Пароль пользователя')
