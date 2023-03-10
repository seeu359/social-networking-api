from datetime import datetime, timedelta

import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from loguru import logger
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from api.db import Session, get_session
from api.posts import models as post_models
from api.settings import settings
from api.users import models, schemes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login')


def get_current_user(token: str = Depends(oauth2_scheme)) -> models.User:

    return UserServices.verify_token(token)


class UserServices:

    @classmethod
    def verify_token(cls, token: str) -> models.User:

        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )

        try:
            payload = jwt.decode(
                token,
                key=settings.secret_key,
                algorithms=settings.algorithm,
            )
        except JWTError:
            raise exception

        user_data = payload.get('user')

        try:
            user = schemes.User.parse_obj(user_data)
        except ValidationError:
            raise exception

        return user

    @classmethod
    def is_valid_password(cls, password, password_hash):

        return bcrypt.verify(password, password_hash)

    @classmethod
    def get_hash_password(cls, password) -> str:

        return bcrypt.hash(password)

    @classmethod
    def hunter_email_verify(cls, email: str) -> None:
        """
        Verify email by hunter.io service
        """
        if not settings.hunter_api_key:
            return

        hunter_api_url = 'https://api.hunter.io/v2/email-verifier?' \
                         'email={}&api_key={}'.format(email,
                                                      settings.hunter_api_key)

        response = requests.get(hunter_api_url).json()
        _status = response['data']['status']
        logger.info(_status)

        if _status == 'invalid' or _status == 'disposable':
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='The email entered does not exist or is temporary'
            )

    @classmethod
    def create_jwt_token(cls, user_data: models.User) -> schemes.Token:

        user = schemes.User.from_orm(user_data)
        user.created_at = str(user.created_at)
        time_now = datetime.utcnow()

        payload = {
            'exp': time_now + timedelta(hours=settings.expiration),
            'sub': str(user.id),
            'nbf': time_now,
            'iat': time_now,
            'user': user.dict(),
        }

        logger.info(payload)
        token = jwt.encode(
            payload,
            key=settings.secret_key,
            algorithm=settings.algorithm
        )

        return schemes.Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):

        self.session = session

    def _create_like_and_dislike(self, user_id):

        like = post_models.Like(user_id=user_id)
        dislike = post_models.Dislike(user_id=user_id)
        self.session.add_all([like, dislike])
        self.session.commit()

    def create_user(self, user_data: schemes.CreateUser) -> schemes.Token:
        self.hunter_email_verify(user_data.email)

        user = models.User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            username=user_data.username,
            email=user_data.email,
            password=self.get_hash_password(user_data.password),
        )

        try:
            self.session.add(user)
            self.session.commit()

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Email or username already exist'
            )

        token = self.create_jwt_token(user)
        self._create_like_and_dislike(user.id)

        return token

    def authenticate_user(self, username: str, password: str) -> schemes.Token:

        exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect username or password',
                headers={'WWW-Authenticate': 'Bearer'},
            )

        user: models.User = self.session.\
            query(models.User).\
            filter(models.User.username == username)\
            .first()

        if not user:
            raise exception

        if not self.is_valid_password(password, user.password):
            raise exception

        return self.create_jwt_token(user)

    def get_user(self, self_username, username: str) -> schemes.ConstructUser:

        if self_username == username:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Entered username must be different from yours',
            )

        user = self.session.query(models.User).where(
            models.User.username == username
        ).first()

        if not user:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User was not found"
            )

        return schemes.ConstructUser.from_orm(user)

    def get_all_users(self) -> list[schemes.ConstructUser] | list:

        users = self.session.query(models.User).\
            where(
            models.User.hidden == False  # noqa: E712
        ).all()

        if not users:
            return list()

        return [schemes.ConstructUser.from_orm(user) for user in users]
