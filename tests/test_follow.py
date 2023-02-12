import json
import pytest
from http import HTTPStatus

from flask_login import login_user
from sqlalchemy import null

from controller.user import user_controller
from form.comment import CommentForm
from app import create_app
from tests.test_fixture import client


def test_follow(client):
    response = client.post('/follow/test_user')
    assert response.status_code == 401

    user = user_controller.get_user(2)
    login_user(user)

    response = client.post('/follow/test_user')

    expected_data = {
        "msg": "Started following test_user."
    }

    if response.status_code == 403:
        assert b'Already following the user.' in response.data
        return
    else:
        response_data = json.loads(response.data)
        for key, value in expected_data.items():
            assert response_data.get(key) == value
        assert response.status_code == HTTPStatus.OK


def test_follow_yourself(client):
    response = client.post('/follow/test_user')
    assert response.status_code == 401

    user = user_controller.get_user(1)
    login_user(user)

    response = client.post('/follow/test_user')

    assert response.status_code == 403
    assert b'You cannot follow yourself.' in response.data


def test_unfollow(client):
    response = client.delete('/unfollow/test_user')
    assert response.status_code == 401

    user = user_controller.get_user(2)
    login_user(user)

    response = client.delete('/unfollow/test_user')

    expected_data = {
        "msg": "Unfollowed test_user."
    }
    if response.status_code == 403:
        assert b'Not following this user.' in response.data
        return
    else:
        response_data = json.loads(response.data)
        for key, value in expected_data.items():
            assert response_data.get(key) == value
        assert response.status_code == HTTPStatus.OK
    response_data = json.loads(response.data)
    for key, value in expected_data.items():
        assert response_data.get(key) == value
    assert response.status_code == HTTPStatus.OK


def test_get_user_followers(client):
    response = client.get('/test_user/followers')
    assert response.status_code == 401

    user = user_controller.get_user(1)
    login_user(user)

    response = client.get('/test_user/followers')

    expected_data = {"followers": ["test_user_second"]}

    expected_data_zero_followers = {"followers": []}

    response_data = json.loads(response.data)
    if expected_data.get("followers") == response_data.get("followers"):
        assert response.status_code == HTTPStatus.OK

    elif expected_data_zero_followers.get("followers") == response_data.get("followers"):
        assert response.status_code == HTTPStatus.OK


def test_get_user_following(client):
    response = client.get('/test_user_second/following')
    assert response.status_code == 401

    user = user_controller.get_user(1)
    login_user(user)

    response = client.get('/test_user_second/following')

    expected_data = {"following list": ["test_user"]}

    expected_data_zero_following = {"following list": []}

    response_data = json.loads(response.data)
    if expected_data.get("following list") == response_data.get("following list"):
        assert response.status_code == HTTPStatus.OK

    elif expected_data_zero_following.get("following list") == response_data.get("following list"):
        assert response.status_code == HTTPStatus.OK


def test_feed(client):
    response = client.get('/feed')
    assert response.status_code == 401

    user = user_controller.get_user(2)
    login_user(user)

    response = client.get('/feed')

    expected_data = {
        "feed posts": [
            [
                {
                    "author_id": 1,
                    "caption": "test again",
                    "content": "http://localhost/test-image.png",
                    "post_id": 1
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
            "author_id": 1,
            "caption": "test again",
            "content": "http://localhost/test-image.png",
            "post_id": 1
        }
    ]
    response_data = json.loads(response.data)
    for expected, response in zip(expected_data, response_data):
        for key, value in expected.items():
            assert response.get(key) == value


def test_get_user_by_username(client):
    response = client.get('/test_user')
    assert response.status_code == 401

    user = user_controller.get_user(1)
    login_user(user)

    response = client.get('/test_user')

    expected_data = {
        "bio": "user info",
        "email": "test@gmail.com",
        "followers_count": 1,
        "following_count": 1,
        "full_name": "Test",
        "posts": [
            {
                "author_id": 1,
                "caption": "test again",
                "content": "http://localhost/test-image.png",
                "post_id": 1
            }
        ],
        "posts_count": 1,
        "profile_pic": "http://localhost/test_profile_pic.png",
        "username": "test_user"
    }

    response_data = json.loads(response.data)
    for key, value in expected_data.items():
        assert response_data.get(key) == value
    assert response.status_code == HTTPStatus.OK
