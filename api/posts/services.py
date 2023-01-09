from fastapi import Depends, HTTPException, status
from sqlalchemy import or_

from api.db import Session, get_session
from api.posts import models, schemes
from api.users.models import User as UserDB
from api.users.schemes import User as UserSchema


class PostService:

    def __init__(self, session: Session = Depends(get_session)):

        self.session = session

    def _get_user_like_and_dislike(
            self, user_id
    ) -> tuple[models.Like, models.Dislike]:

        like = self.session.query(
            models.Like
        ).where(models.Like.user_id == user_id).first()

        dislike = self.session.query(
            models.Dislike
        ).where(models.Dislike.user_id == user_id).first()

        return like, dislike

    @classmethod
    def get_post_scheme(
            cls, post_orm: models.Post, likes_count: int = 0,
            dislikes_count: int = 0,
    ) -> schemes.Post:

        return schemes.Post(
            id=post_orm.id,
            author_id=post_orm.user_id,
            title=post_orm.title,
            user_id=post_orm.user_id,
            post_body=post_orm.post_body,
            created_at=post_orm.created_at,
            hidden=post_orm.hidden,
            likes=likes_count,
            dislikes=dislikes_count,
        )

    def _get_post(self, post_id: int) -> models.Post:

        post = self.session.\
            query(models.Post).\
            filter(models.Post.id == post_id).\
            first()

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='The post was not found',
            )

        return post

    def create_post(
            self, post_data: schemes.CreatePost, user_id: int
    ) -> schemes.Post:

        post = models.Post(
            user_id=user_id,
            title=post_data.title,
            post_body=post_data.post_body,
            hidden=post_data.hidden,
        )

        self.session.add(post)
        self.session.commit()

        post_scheme = self.get_post_scheme(post)

        return post_scheme

    def get_all_posts(self, user_id: int) -> list[schemes.Post] | list[...]:
        """Return list of Posts, besides posts which hidden field is True.
        Posts which have hidden field is True, can view only friends.
        """
        posts: list[models.Post] = self.session.query(models.Post).where(
            or_(models.Post.hidden == False,  # noqa: E712
                models.Post.user_id == user_id
                )).all()

        if not posts:
            return list()

        return [self.get_post_scheme(
            post, post.likes_count(), post.dislikes_count()
        ) for post in posts]

    def get_post(self, user_id: int, post_id: int):

        post = self._get_post(post_id)

        if post.hidden:
            if user_id == post_id:
                return self.get_post_scheme(
                    post, post.likes_count(), post.dislikes_count()
                )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You have no permission to view this post',
            )

        return self.get_post_scheme(
            post, post.likes_count(), post.dislikes_count()
        )

    def delete_post(self, user_id: int, post_id: int) -> list:

        post = self._get_post(post_id)

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='The post was not found',
            )

        if post.user_id == user_id:
            post.clear_refs()
            self.session.delete(post)
            self.session.commit()
            return list()

        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You can\'t delete post they aren\'t yours',
            )

    def update_post(
            self, post_data, user_id: int, post_id: int
    ) -> schemes.Post:

        post = self._get_post(post_id)

        if post.user_id == user_id:
            post.title = post_data.title
            post.post_body = post_data.post_body
            post.hidden = post_data.hidden
            self.session.commit()
            return self.get_post_scheme(
                post, post.likes_count(), post.dislikes_count(),
            )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You can\'t edit post they aren\'t yours',
        )

    def put_like(self, user_id: int, post_id: int) -> schemes.Post:

        post = self._get_post(post_id)

        users_like, users_dislike = self._get_user_like_and_dislike(user_id)

        if user_id == post.user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='It is impossible to rate your own posts'
            )

        if users_like in post.likes:

            post.likes.remove(users_like)
            self.session.commit()
            return self.get_post_scheme(
                post, post.likes_count(), post.dislikes_count()
            )

        if users_dislike in post.dislikes:

            post.dislikes.remove(users_dislike)

        post.likes.append(users_like)
        self.session.commit()
        return self.get_post_scheme(
            post, post.likes_count(), post.dislikes_count()
        )

    def put_dislike(self, user_id: int, post_id: int) -> schemes.Post:

        post = self._get_post(post_id)

        users_like, users_dislike = self._get_user_like_and_dislike(user_id)

        if user_id == post.user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='It is impossible to rate your own posts'
            )

        if users_dislike in post.dislikes:

            post.dislikes.remove(users_dislike)
            self.session.commit()
            return self.get_post_scheme(
                post, post.likes_count(), post.dislikes_count()
            )
        if users_like in post.likes:

            post.likes.remove(users_like)

        post.dislikes.append(users_dislike)
        self.session.commit()
        return self.get_post_scheme(
            post, post.likes_count(), post.dislikes_count()
        )

    def get_post_likes(self, post_id: int) -> list[UserSchema] | list:

        post = self._get_post(post_id)
        users_id = [like.user_id for like in post.likes]
        users = self.session.query(UserDB).filter(
            UserDB.id.in_(users_id)
        ).all()

        return [UserSchema.from_orm(user) for user in users]

    def get_post_dislikes(self, post_id: int) -> list[UserSchema] | list:

        post = self._get_post(post_id)
        users_id = [dislike.user_id for dislike in post.dislikes]
        users = self.session.query(UserDB).filter(
            UserDB.id.in_(users_id)
        ).all()

        return [UserSchema.from_orm(user) for user in users]
