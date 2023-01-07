import loguru
from fastapi import Depends, HTTPException, status
from sqlalchemy import or_
from loguru import logger

from api.db import Session, get_session
from api.posts import models, schemes
from api.users.schemes import User as UserSchema
from api.users.models import User as UserDB


class PostService:

    def __init__(self, session: Session = Depends(get_session)):

        self.session = session

    def _get_users_rate(self, user_id: int, post_id: int):

        return self.session.query(models.UserLikes). \
            filter(
            models.UserLikes.user_id == user_id,
            models.UserLikes.post_id == post_id,
        ).first()

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

        post_scheme = schemes.Post.from_orm(post)
        return post_scheme

    def get_all_posts(self, user_id: int) -> list[schemes.Post]:
        """Return list of Posts, besides posts which hidden field is True.
        Posts which have hidden field is True, can view only friends.
        """
        posts = self.session.query(models.Post).where(
            or_(models.Post.hidden == 0,
                models.Post.user_id == user_id
                )).all()
        return [schemes.Post.from_orm(post) for post in posts]

    def get_post(self, user_id: int, post_id: int):

        post = self._get_post(post_id)

        if post.hidden:
            if user_id == post_id:
                return schemes.Post.from_orm(post)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You have no permission to view this post',
            )

        return schemes.Post.from_orm(post)

    def delete_post(self, user_id: int, post_id: int) -> list:

        post = self._get_post(post_id)

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='The post was not found',
            )
        if post.user_id == user_id:
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
            return schemes.Post.from_orm(post)

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You can\'t edit post they aren\'t yours',
        )

    def put_like(self, user_id: int, post_id: int) -> schemes.Post:

        post = self._get_post(post_id)

        if user_id == post.user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='It is impossible to rate your own posts'
            )

        users_rate = self._get_users_rate(user_id, post_id)
        loguru.logger.info(users_rate)

        if not users_rate:

            like = models.UserLikes(
                user_id=user_id,
                post_id=post_id,
                like=True,
                dislike=False,
            )
            post.likes += 1
            self.session.add(like)
            loguru.logger.info(schemes.Post.from_orm(post))
            self.session.commit()
            return schemes.Post.from_orm(post)

        else:

            if users_rate.like:

                self.session.delete(users_rate)
                post.likes -= 1
                self.session.commit()
                return schemes.Post.from_orm(post)

            if users_rate.dislike:

                users_rate.like = True
                users_rate.dislike = False
                post.likes += 1
                post.dislikes -= 1
                self.session.commit()
                return schemes.Post.from_orm(post)

    def put_dislike(self, user_id: int, post_id: int) -> schemes.Post:

        post = self._get_post(post_id)

        if user_id == post.user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='It is impossible to rate your own posts'
            )

        users_rate = self._get_users_rate(user_id, post_id)

        if not users_rate:

            dislike = models.UserLikes(
                user_id=user_id,
                post_id=post_id,
                like=False,
                dislike=True,
            )
            post.dislikes += 1
            self.session.add(dislike)
            loguru.logger.info(schemes.Post.from_orm(post))
            self.session.commit()
            return schemes.Post.from_orm(post)

        else:

            if users_rate.like:

                users_rate.dislike = True
                users_rate.like = False
                post.dislikes += 1
                post.likes -= 1
                self.session.commit()
                return schemes.Post.from_orm(post)

            if users_rate.dislike:

                self.session.delete(users_rate)
                post.dislikes -= 1
                self.session.commit()
                return schemes.Post.from_orm(post)

    def get_post_likes(self, post_id: int) -> list[UserSchema] | list[...]:

        self._get_post(post_id)

        post_likes = self.session.\
            query(models.UserLikes).\
            filter(models.UserLikes.like == 1,
                   models.UserLikes.post_id == post_id).\
            all()
        logger.info(post_likes)

        if not post_likes:
            return list()

        users_id = [user.user_id for user in post_likes]
        logger.info(users_id)
        users = self.session.query(UserDB).filter(
            UserDB.id.in_(users_id)
        ).all()

        return [UserSchema.from_orm(user) for user in users]
