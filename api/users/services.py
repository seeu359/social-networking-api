from fastapi import Depends
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.hash import bcrypt
import json
from loguru import logger
from api.db import Session, get_session
from api.users import schemes
from api.models import User
from api.settings import settings


class UserServices:

    @classmethod
    def get_hash_password(cls, password) -> str:

        return bcrypt.hash(password)

    @classmethod
    def create_jwt_token(cls, user_data) -> schemes.Token:
        user = schemes.User.from_orm(user_data)
        user.created_at = str(user.created_at)
        time_now = datetime.utcnow()
        payload = {
            'exp': str(time_now + timedelta(seconds=settings.expiration)),
            'sub': user.id,
            'aud': 'users',
            'nbf': str(time_now),
            'iat': str(time_now),
            'user': user.dict()
        }
        logger.info(payload)
        token = jwt.encode(
            payload,
            key=settings.secret_key,
            algorithm=settings.algorithm
        )
        return schemes.Token(token=token)

    def __init__(self, session: Session = Depends(get_session)):

        self.session = session

    def create_user(self, user_data: schemes.CreateUser) -> schemes.Token:

        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            username=user_data.username,
            email=user_data.email,
            password=self.get_hash_password(user_data.password),
        )
        self.session.add(user)
        self.session.commit()
        token = self.create_jwt_token(user)
        return token
