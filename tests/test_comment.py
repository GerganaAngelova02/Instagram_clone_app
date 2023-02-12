import json
import pytest
from http import HTTPStatus

from flask_login import login_user

from controller.user import user_controller
from form.comment import CommentForm
from app import create_app
from tests.test_fixture import client


def test_create_comment(client):
    response = client.post('/post/1/comment')
    assert response.status_code == 401

    user = user_controller.get_user(2)
    login_user(user)

    form = CommentForm(prefix='form-comment-')
    response = client.post(
        '/post/1/comment', data={'comment': 'nice'})

    expected_data = {
        "id": 1,
        "comment": "nice",
        "user_id": 2,
        "post_id": 1
    }

    response_data = json.loads(response.data)
    for key, value in expected_data.items():
        assert response_data.get(key) == value
    assert response.status_code == 200


def test_get_comments(client):
    response = client.get('/post/1/comments')
    assert response.status_code == 401

    user = user_controller.get_user(1)
    login_user(user)

    response = client.get('/post/1/comments')

    expected_data = [
        {
            "comment": "nice",
            "username": "test_user_second"
        }
    ]

    response_data = json.loads(response.data)
    for expected, response in zip(expected_data, response_data):
        for key, value in expected.items():
            assert response.get(key) == value


def test_get_comment(client):
    response = client.get('/post/1/comment/1')
    assert response.status_code == 401

    user = user_controller.get_user(1)
    login_user(user)

    response = client.get('/post/1/comment/1')

    expected_data = {
        "comment": "nice",
        "id": 1,
        "post_id": 1,
        "user_id": 2
    }

    response_data = json.loads(response.data)
    for key, value in expected_data.items():
        assert response_data.get(key) == value
    assert response.status_code == 200


def test_delete_comment(client):
    response = client.delete('/post/1/comment/1')
    assert response.status_code == 401

    user = user_controller.get_user(1)
    login_user(user)

    response = client.delete('/post/1/comment/1')

    assert response.status_code == 200


# for this test we need third user so make sure it is created
def test_delete_comment_not_authorised(client):
    response = client.delete('/post/1/comment/1')
    assert response.status_code == 401

    user = user_controller.get_user(3)
    login_user(user)

    response = client.delete('/post/1/comment/1')

    assert response.status_code == 404
    assert b'You can not delete this comment!' in response.data


def test_update_comment(client):
    response = client.post('/post/1/comment/1')
    assert response.status_code == 401

    user = user_controller.get_user(2)
    login_user(user)

    form = CommentForm(prefix='form-comment-')

    response = client.post('/post/1/comment/1', data={'comment': 'good'})

    assert response.status_code == 200


def test_update_comment_not_authorised(client):
    response = client.post('/post/1/comment/1')
    assert response.status_code == 401

    user = user_controller.get_user(3)
    login_user(user)

    form = CommentForm(prefix='form-comment-')

    response = client.post('/post/1/comment/1', data={'comment': 'good'})
    assert response.status_code == 404
    assert b'You can not update this comment!' in response.data
