from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from loguru import logger
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from api.db import Session, get_session
from api.settings import settings
from api.users import models, schemes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login/')


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
    def create_jwt_token(cls, user_data: models.User) -> schemes.Token:

        user = schemes.User.from_orm(user_data)
        user.created_at = str(user.created_at)
        time_now = datetime.utcnow()

        payload = {
            'exp': time_now + timedelta(seconds=settings.expiration),
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

    def create_user(self, user_data: schemes.CreateUser) -> schemes.Token:
        print(user_data)
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
