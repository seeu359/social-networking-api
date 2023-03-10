from datetime import datetime

from pydantic import BaseModel


class Post(BaseModel):

    id: int
    author_id: int
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
