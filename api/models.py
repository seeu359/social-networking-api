import datetime

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from api.db import engine

Base = declarative_base()


class User(Base):

    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.String, nullable=False)
    last_name = sa.Column(sa.String, nullable=False)
    username = sa.Column(sa.String, unique=True, nullable=False)
    password = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, unique=True, nullable=False)
    hidden = sa.Column(sa.Boolean, default=False)
    created_at = sa.Column(sa.Date, default=datetime.date.today())
