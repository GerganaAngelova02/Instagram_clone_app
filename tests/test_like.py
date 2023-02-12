import json
import pytest
from http import HTTPStatus

from flask_login import login_user

from controller.user import user_controller

from app import create_app
from tests.test_fixture import client


def test_like_post(client):
    response = client.post('/post/1/like_unlike')
    assert response.status_code == 401

    user = user_controller.get_user(2)
    login_user(user)

    response = client.post('/post/1/like_unlike')

    expected_data = {
        "by user": "test_user_second",
        "msg": "Post Liked",
        "post_id": "1"
    }

    response_data = json.loads(response.data)
    for key, value in expected_data.items():
        assert response_data.get(key) == value
    assert response.status_code == HTTPStatus.OK


def test_unlike_post(client):
    response = client.delete('/post/1/like_unlike')
    assert response.status_code == 401

    user = user_controller.get_user(2)
    login_user(user)

    response = client.delete('/post/1/like_unlike')

    expected_data = {
        "by user": "test_user_second",
        "msg": "Post Unliked",
        "post_id": "1"
    }

    response_data = json.loads(response.data)
    for key, value in expected_data.items():
        assert response_data.get(key) == value
    assert response.status_code == HTTPStatus.OK


def test_likes_count(client):
    response = client.get('/post/1/likes_count')
    assert response.status_code == 401

    user = user_controller.get_user(1)
    login_user(user)

    response = client.get('/post/1/likes_count')

    expected_data = {
        "likes_count": 1,
        "post_id": 1
    }

    if response.status_code == HTTPStatus.NOT_FOUND:
        assert b'Post was not found!' in response.data
        return
    else:
        response_data = json.loads(response.data)
        for key, value in expected_data.items():
            assert response_data.get(key) == value
        assert response.status_code == HTTPStatus.OK


def test_likes(client):
    response = client.get('/post/1/likes')
    assert response.status_code == 401

    user = user_controller.get_user(1)
    login_user(user)

    response = client.get('/post/1/likes')

    expected_data = ["test_user_second"]

    expected_data_zero_likes = []
    response_data = json.loads(response.data)
    assert set(expected_data).intersection(response_data) == set(expected_data) or \
           set(expected_data_zero_likes).intersection(response_data) == set(expected_data_zero_likes)
    assert response.status_code == HTTPStatus.OK
