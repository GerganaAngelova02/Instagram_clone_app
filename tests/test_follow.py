import json
import pytest
from http import HTTPStatus

from flask_login import login_user

from controller.user import user_controller
from form.comment import CommentForm
from app import create_app
from tests.test_fixture import client


def test_follow(client):
    response = client.post('/follow/test_test')
    assert response.status_code == 401

    user = user_controller.get_user(18)
    login_user(user)

    response = client.post('/follow/test_test')

    expected_data = {
        "msg": "Started following test_test."
    }

    response_data = json.loads(response.data)
    for key, value in expected_data.items():
        assert response_data.get(key) == value
    assert response.status_code == HTTPStatus.OK


def test_unfollow(client):
    response = client.delete('/unfollow/test_test')
    assert response.status_code == 401

    user = user_controller.get_user(18)
    login_user(user)

    response = client.delete('/unfollow/test_test')

    expected_data = {
        "msg": "Unfollowed test_test."
    }

    response_data = json.loads(response.data)
    for key, value in expected_data.items():
        assert response_data.get(key) == value
    assert response.status_code == HTTPStatus.OK


def test_get_user_followers(client):
    response = client.get('/test_test/followers')
    assert response.status_code == 401

    user = user_controller.get_user(18)
    login_user(user)

    response = client.get('/test_test/followers')

    expected_data = {
        "followers": [
            "nia_dimitrova",
            "test_user"
        ]
    }

    response_data = json.loads(response.data)
    for key, value in expected_data.items():
        assert response_data.get(key) == value
    assert response.status_code == HTTPStatus.OK


def test_get_user_following(client):
    response = client.get('/test_test/following')
    assert response.status_code == 401

    user = user_controller.get_user(18)
    login_user(user)

    response = client.get('/test_test/following')

    expected_data = {
        "following list": [
            "nia_dimitrova"
        ]
    }

    response_data = json.loads(response.data)
    for key, value in expected_data.items():
        assert response_data.get(key) == value
    assert response.status_code == HTTPStatus.OK


def test_feed(client):
    response = client.get('/feed')
    assert response.status_code == 401

    user = user_controller.get_user(18)
    login_user(user)

    response = client.get('/feed')

    expected_data = {
        "feed posts": [
            [
                {
                    "author_id": 7,
                    "caption": "test",
                    "content": "http://localhost:5000/test-image.png",
                    "post_id": 22
                }
            ]
        ]
    }

    response_data = json.loads(response.data)
    for key, value in expected_data.items():
        assert response_data.get(key) == value
    assert response.status_code == HTTPStatus.OK


def test_explore(client):
    response = client.get('/explore')
    assert response.status_code == 401

    user = user_controller.get_user(1)
    login_user(user)

    response = client.get('/explore')

    expected_data = [
        {
            "author_id": 7,
            "caption": "test",
            "content": "http://localhost:5000/test-image.png",
            "post_id": 22
        }
    ]

    response_data = json.loads(response.data)
    for expected, response in zip(expected_data, response_data):
        for key, value in expected.items():
            assert response.get(key) == value
