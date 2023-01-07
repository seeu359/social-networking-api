from datetime import datetime

from pydantic import BaseModel, Field


class Post(BaseModel):

    id: int
    author: int = Field(alias='user_id')
    title: str
    post_body: str
    created_at: datetime
    hidden: bool
    likes: int
    dislikes: int

    class Config:

        orm_mode = True


class CreatePost(BaseModel):

    title: str
    post_body: str
    hidden: bool = False


class UpdatePost(CreatePost):
    pass
