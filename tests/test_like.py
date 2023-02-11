import json
import pytest
from http import HTTPStatus

from flask_login import login_user

from controller.user import user_controller

from app import create_app
from tests.test_fixture import client


def test_like_post(client):
    response = client.post('/post/22/like_unlike')
    assert response.status_code == 401

    user = user_controller.get_user(18)
    login_user(user)

    response = client.post('/post/22/like_unlike')

    expected_data = {
        "by user": "test_user",
        "msg": "Post Liked",
        "post_id": "22"
    }

    response_data = json.loads(response.data)
    for key, value in expected_data.items():
        assert response_data.get(key) == value
    assert response.status_code == HTTPStatus.OK


def test_unlike_post(client):
    response = client.delete('/post/22/like_unlike')
    assert response.status_code == 401

    user = user_controller.get_user(18)
    login_user(user)

    response = client.delete('/post/22/like_unlike')

    expected_data = {
        "by user": "test_user",
        "msg": "Post Unliked",
        "post_id": "22"
    }

    response_data = json.loads(response.data)
    for key, value in expected_data.items():
        assert response_data.get(key) == value
    assert response.status_code == HTTPStatus.OK


def test_likes_count(client):
    response = client.get('/post/22/likes_count')
    assert response.status_code == 401

    user = user_controller.get_user(18)
    login_user(user)

    response = client.get('/post/22/likes_count')

    expected_data = {
        "likes_count": 1,
        "post_id": 22
    }

    response_data = json.loads(response.data)
    for key, value in expected_data.items():
        assert response_data.get(key) == value
    assert response.status_code == HTTPStatus.OK


def test_likes(client):
    response = client.get('/post/22/likes')
    assert response.status_code == 401

    user = user_controller.get_user(18)
    login_user(user)

    response = client.get('/post/22/likes')

    expected_data = [
        "test_user"
    ]

    response_data = json.loads(response.data)
    assert set(expected_data).intersection(response_data) == set(expected_data)
    assert response.status_code == HTTPStatus.OK
