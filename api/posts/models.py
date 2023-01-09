from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped

from api import Base
from api.db import engine, Session
from api.users.models import User


like_refs = sa.Table(
    'like_ref',
    Base.metadata,
    sa.Column('post_id', sa.ForeignKey('post.id'), primary_key=True),
    sa.Column('like_id', sa.ForeignKey('like.id'), primary_key=True),
)

dislike_refs = sa.Table(
    'dislike_ref',
    Base.metadata,
    sa.Column('post_id', sa.ForeignKey('post.id'), primary_key=True),
    sa.Column('dislike_id', sa.ForeignKey('dislike.id'), primary_key=True),
)


class Post(Base):

    __tablename__ = 'post'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=False)
    post_body = sa.Column(sa.Text, nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), nullable=False)
    created_at = sa.Column(
        sa.DateTime, nullable=False, default=datetime.now()
    )
    hidden = sa.Column(sa.Boolean, default=False)
    likes = relationship(
        'Like',
        secondary=like_refs,
        back_populates='like',
    )
    dislikes = relationship(
        'Dislike',
        secondary=dislike_refs,
        back_populates='dislike',
    )

    def likes_count(self):

        return len(self.likes)

    def dislikes_count(self):

        return len(self.dislikes)

    def clear_refs(self):
        """
        Clear posts likes and  posts dislikes refs during deletion post
        """
        self.likes.clear()
        self.dislikes.clear()


class Like(Base):

    __tablename__ = 'like'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    like = relationship(
        'Post', secondary=like_refs, back_populates='likes',
    )


class Dislike(Base):

    __tablename__ = 'dislike'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), nullable=False)

    dislike = relationship(
        'Post', secondary=dislike_refs, back_populates='dislikes',
    )
