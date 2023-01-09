import os

from fastapi import status
from fastapi.testclient import TestClient

from api.db import get_session
from main import app
from api.settings import settings
from api.users.services import get_current_user
from tests.conftest import (MockValidUser, get_mock_session,
                            mock_current_invalid_user)

client = TestClient(app)


def test_users_me():

    app.dependency_overrides[get_current_user] = MockValidUser
    response = client.get('/users/me')

    assert response.status_code == 200


def test_not_valid_user_data():

    app.dependency_overrides[get_current_user] = mock_current_invalid_user
    response = client.get('/users/me')

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_and_login_user(mock_create_user_data, mock_create_user_data2):

    app.dependency_overrides[get_session] = get_mock_session

    user1 = client.post(
        '/users/create',
        json=mock_create_user_data,
    )
    user2 = client.post(
        '/users/create',
        json=mock_create_user_data2,
    )

    os.remove(settings.test_database_path)
    assert user1.status_code == status.HTTP_201_CREATED
    assert user2.status_code == status.HTTP_201_CREATED
