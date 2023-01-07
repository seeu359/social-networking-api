from datetime import datetime

import sqlalchemy as sa

from api import Base


class UserLikes(Base):

    __tablename__ = 'user_likes'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    post_id = sa.Column(sa.Integer, sa.ForeignKey('post.id'))
    like = sa.Column(sa.Boolean, default=False)
    dislike = sa.Column(sa.Boolean, default=False)


class Post(Base):

    __tablename__ = 'post'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=False)
    post_body = sa.Column(sa.Text, nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    created_at = sa.Column(
        sa.DateTime, nullable=False, default=datetime.now()
    )
    hidden = sa.Column(sa.Boolean, default=False)
    likes = sa.Column(sa.Integer, default=0)
    dislikes = sa.Column(sa.Integer, default=0)
