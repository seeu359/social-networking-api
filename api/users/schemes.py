from datetime import date

from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, validator


class BaseUser(BaseModel):

    first_name: str
    last_name: str
    username: str
    email: EmailStr

    @validator('first_name', 'last_name',)
    def validate_name(cls, value: str):

        if not value.isalpha():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='First name and last name must contains only letters'
            )
        else:
            return value


class User(BaseUser):

    id: int
    hidden: bool
    created_at: date

    class Config:

        orm_mode = True


class CreateUser(BaseUser):

    password: str


class Token(BaseModel):

    access_token: str
    token_type: str = 'bearer'
