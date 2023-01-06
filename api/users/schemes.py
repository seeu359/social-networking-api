from pydantic import BaseModel
from datetime import date


class BaseUser(BaseModel):

    first_name: str
    last_name: str
    username: str
    email: str


class User(BaseUser):

    id: int
    hidden: bool
    created_at: date

    class Config:

        orm_mode = True


class CreateUser(BaseUser):

    password: str


class Token(BaseModel):

    token: str
    token_type: str = 'bearer'
