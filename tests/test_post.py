import json
import pytest
from http import HTTPStatus
from io import BytesIO
from flask_login import login_user
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from model.post import Post
from form.post_form import PostForm
from controller.user import user_controller
import os
from app import create_app
from tests.test_fixture import client


def test_upload(client):
    response = client.post('/upload')
    assert response.status_code == 401

    user = user_controller.get_user(1)
    login_user(user)

    file_path = os.path.join(client.application.root_path, 'content', 'test-image.png')

    form = PostForm(prefix='form-data-')

    with open(file_path, 'rb') as f:
        file_contents = f.read()
        response = client.post('/upload', data={'caption': 'testing',
                                                'content': (BytesIO(file_contents), 'test-image.png')})

        assert response.status_code == 200


def test_get_all_posts(client):
    response = client.get('/posts')
    assert response.status_code == 401

    user = user_controller.get_user(1)
    login_user(user)

    response = client.get('/posts')

    expected_data = [
        {
            "author_id": 1,
            "caption": "testing",
            "content": "http://localhost/test-image.png",
            "post_id": 1
        }
    ]

    response_data = json.loads(response.data)
    for expected, response in zip(expected_data, response_data):
        for key, value in expected.items():
            assert response.get(key) == value


def test_get_post(client):
    response = client.get('/post/1')
    assert response.status_code == 401

    user = user_controller.get_user(1)
    login_user(user)

    response = client.get('/post/1')

    expected_data = {
        "author_id": 1,
        "caption": "testing",
        "content": "http://localhost/test-image.png",
        "post_id": 1
    }

    response_data = json.loads(response.data)
    for key, value in expected_data.items():
        assert response_data.get(key) == value
    assert response.status_code == HTTPStatus.OK


def test_update_post(client):
    response = client.post('/post/1')
    assert response.status_code == 401

    user = user_controller.get_user(1)
    login_user(user)

    form = PostForm(prefix='form-data-')

    response = client.post('/post/1', data={'caption': 'test again'})

    assert response.status_code == 200


def test_delete_post(client):
    response = client.delete('/post/1')
    assert response.status_code == 401

    user = user_controller.get_user(1)
    login_user(user)

    response = client.delete('/post/1')

    assert response.status_code == 200


def test_delete_post_not_author(client):
    response = client.delete('/post/1')
    assert response.status_code == 401

    user = user_controller.get_user(2)
    login_user(user)

    response = client.delete('/post/1')
    assert response.status_code == 404
    assert b'This post can not be deleted' in response.data
