import os

from fastapi import status
from fastapi.testclient import TestClient

from api.db import get_session
from api.main import app
from api.settings import settings
from api.users.services import get_current_user
from tests.conftest import MockValidUser, MockValidUser2, get_mock_session

app.dependency_overrides[get_session] = get_mock_session
app.dependency_overrides[get_current_user] = MockValidUser

client = TestClient(app)


def test_create_post(test_post_data):

    response = client.post(
        'posts/create',
        json=test_post_data
    )

    os.remove(settings.test_database_path)
    assert response.status_code == status.HTTP_201_CREATED


def test_update_post(test_post_data):

    post = client.post(
        'posts/create',
        json={
            'title': 'title',
            'post_body': 'test',
            'hidden': True,
        }
    )

    post_id = post.json()['id']

    response = client.put(
        '/posts/{}'.format(post_id),
        json=test_post_data
    )

    os.remove(settings.test_database_path)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == 'test title'
    assert response.json()['id'] == 1


def test_update_post_that_is_not_your_own(test_post_data):

    post = client.post(
        '/posts/create',
        json=test_post_data,
    )

    post_id = post.json()['id']
    app.dependency_overrides[get_current_user] = MockValidUser2

    response = client.put(
        '/posts/{}'.format(post_id),
        json=test_post_data,
    )

    app.dependency_overrides[get_current_user] = MockValidUser
    os.remove(settings.test_database_path)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_all_posts(test_post_data):

    post_count = 3

    for _ in range(3):
        client.post(
            '/posts/create',
            json=test_post_data
        )

    response = client.get(
        '/posts',
    )

    os.remove(settings.test_database_path)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == post_count


def test_delete_post(test_post_data):

    post_count = 4

    for i in range(post_count):

        client.post(
            '/posts/create',
            json=test_post_data,
        )

    last_post_id = 4
    response = client.delete(
        '/posts/{}'.format(last_post_id),
    )

    all_post = client.get(
        '/posts'
    )

    os.remove(settings.test_database_path)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert len(all_post.json()) == 3


def test_delete_post_that_is_not_your_own(test_post_data):

    post = client.post(
        '/posts/create',
        json=test_post_data
    )

    post_id = post.json()['id']

    app.dependency_overrides[get_current_user] = MockValidUser2

    response = client.delete(
        '/posts/{}'.format(post_id),
    )

    app.dependency_overrides[get_current_user] = MockValidUser
    os.remove(settings.test_database_path)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_put_like_and_dislike_to_own_post(test_post_data):

    post = client.post(
        '/posts/create',
        json=test_post_data
    )

    post_id = post.json()['id']

    like_response = client.put(
        '/posts/{}/like'.format(post_id),
    )
    dislike_response = client.put(
        '/posts/{}/dislike'.format(post_id)
    )

    os.remove(settings.test_database_path)
    assert like_response.status_code == status.HTTP_409_CONFLICT
    assert dislike_response.status_code == status.HTTP_409_CONFLICT


def test_put_like_and_dislike(test_post_data):

    post = client.post(
        '/posts/create',
        json=test_post_data
    )

    post_id = post.json()['id']

    app.dependency_overrides[get_current_user] = MockValidUser2

    response_like = client.put(
        '/posts/{}/like'.format(post_id)
    )
    assert response_like.status_code == status.HTTP_200_OK
    assert response_like.json()['likes'] == 1
    assert response_like.json()['dislikes'] == 0

    response_dislike = client.put(
        '/posts/{}/dislike'.format(post_id)
    )

    assert response_dislike.status_code == status.HTTP_200_OK
    assert response_dislike.json()['dislikes'] == 1
    assert response_dislike.json()['likes'] == 0
    os.remove(settings.test_database_path)
