from fastapi import Depends, HTTPException, status
from sqlalchemy import or_

from api.db import Session, get_session
from api.posts import models, schemes


class PostService:

    def __init__(self, session: Session = Depends(get_session)):

        self.session = session

    def _get_post(self, post_id: int) -> models.Post:

        return self.session.\
            query(models.Post).\
            filter(models.Post.id == post_id).\
            first()

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

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='The post was not found',
            )

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

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='The post was not found',
            )

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
