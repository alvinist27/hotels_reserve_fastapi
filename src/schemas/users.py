from pydantic import BaseModel, Field, EmailStr


class UserAddRequestSchema(BaseModel):
    email: EmailStr = Field(description='E-mail пользователя')
    password: str = Field(description='Пароль пользователя')


class UserSchema(BaseModel):
    id: int
    email: EmailStr = Field(description='E-mail пользователя')


class UserWithPasswordSchema(UserSchema):
    password: str = Field(description='Пароль пользователя')
