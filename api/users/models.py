from datetime import date

import sqlalchemy as sa

from api import Base


class User(Base):

    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.String, nullable=False)
    last_name = sa.Column(sa.String, nullable=False)
    username = sa.Column(sa.String, unique=True, nullable=False)
    password = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, unique=True, nullable=False)
    hidden = sa.Column(sa.Boolean, default=False)
    created_at = sa.Column(sa.Date, default=date.today())
