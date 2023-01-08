import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api import Base
from api.settings import settings


def get_mock_session():

    engine = create_engine(
        settings.test_database_url, connect_args={"check_same_thread": False}
    )

    Base.metadata.create_all(engine)

    test_session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    session = test_session()
    yield session


class MockValidUser:

    def __init__(self):

        self.id = 1
        self.first_name = 'testname'
        self.last_name = 'testsurname'
        self.hidden = False
        self.username = 'Alex'
        self.created_at = '2022-12-31'
        self.email = 'test@mail.ru'


class MockValidUser2:

    def __init__(self):

        self.id = 2
        self.first_name = 'John'
        self.last_name = 'Doe'
        self.hidden = False
        self.username = 'john'
        self.created_at = '2022-12-31'
        self.email = 'test2@mail.ru'


def mock_current_invalid_user():
    return {
        'id': 1,
        'first_name': 'invalid name',
        'last_name': 'invalid surname',
        'hidden': False,
        'username': 'Alex',
        'created_at': '2022-12-31',
        'email': 'invalidemail'
    }


@pytest.fixture
def mock_create_user_data() -> dict:

    return {
        'first_name': 'Alex',
        'last_name': 'Chere',
        'username': 'testuser',
        'email': 'test@mail.ru',
        'password': 'topsecret',
    }


@pytest.fixture
def test_post_data() -> dict:

    return {
        'title': 'test title',
        'post_body': 'test body',
        'hidden': False,
    }
