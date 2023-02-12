import json
import os
from io import BytesIO
import pytest
from http import HTTPStatus
from tests.test_fixture import client
from flask_login import login_user, logout_user
from model.user import User
from form.user_register_form import RegistrationForm
from form.user_login_form import LoginForm
from form.user_settings_form import SettingsForm
from controller.user import user_controller
from app import create_app


def test_create_user(client):
    form = RegistrationForm(prefix='form-register-')

    response = client.post(
        '/register', data={
            'username': 'test_user',
            'email': 'test@gmail.com',
            'full_name': 'Test',
            'password': 'pass'
        })

    expected_data = {
        'username': 'test_user',
        'email': 'test@gmail.com',
        'full_name': 'Test',
        'password': 'pass'
    }

    if response.status_code == HTTPStatus.BAD_REQUEST:
        assert b'The username is already taken' in response.data \
               or b'The email is already registered' in response.data
        return
    response_data = json.loads(response.data)
    for key, value in expected_data.items():
        assert response_data.get(key) == value
    assert response.status_code == HTTPStatus.OK


# run this to create second user in the database so that the two can interact with each other in the next tests
def test_create_second_user(client):
    form = RegistrationForm(prefix='form-register-')

    response = client.post(
        '/register', data={
            'username': 'test_user_second',
            'email': 'test_second@gmail.com',
            'full_name': 'Test Second',
            'password': 'password'
        })

    expected_data = {
        'username': 'test_user_second',
        'email': 'test_second@gmail.com',
        'full_name': 'Test Second',
        'password': 'password'
    }

    if response.status_code == HTTPStatus.BAD_REQUEST:
        assert b'The username is already taken' in response.data \
               or b'The email is already registered' in response.data
        return
    response_data = json.loads(response.data)
    for key, value in expected_data.items():
        assert response_data.get(key) == value
    assert response.status_code == HTTPStatus.OK


# we need third user when testing deleting of comment
def test_create_user_third(client):
    form = RegistrationForm(prefix='form-register-')

    response = client.post(
        '/register', data={
            'username': 'test_user_third',
            'email': 'test_third@gmail.com',
            'full_name': 'Test Third',
            'password': 'pass 3'
        })

    expected_data = {
        'username': 'test_user_third',
        'email': 'test_third@gmail.com',
        'full_name': 'Test Third',
        'password': 'pass 3'
    }

    if response.status_code == HTTPStatus.BAD_REQUEST:
        assert b'The username is already taken' in response.data \
               or b'The email is already registered' in response.data
        return
    response_data = json.loads(response.data)
    for key, value in expected_data.items():
        assert response_data.get(key) == value
    assert response.status_code == HTTPStatus.OK


def test_login_user_valid(client):
    form = LoginForm(prefix='form-login-')
    response = client.post(
        '/login', data={
            'email': 'test@gmail.com',
            'password': 'pass'
        })
    expected_output_valid = {
        'status': 'success',
        'user': 'test_user',
    }
    response_data = json.loads(response.data)
    for key, value in expected_output_valid.items():
        assert response_data.get(key) == value
    assert response.status_code == HTTPStatus.OK


def test_login_user_invalid(client):
    form = LoginForm(prefix='form-login-')
    response = client.post(
        '/login', data={
            'email': 'invalid@gmail.com',
            'password': 'pass'
        })
    expected_output_invalid = {
        'status': 'fail',
        'message': 'Invalid email or password',
    }
    response_data = json.loads(response.data)
    for key, value in expected_output_invalid.items():
        assert response_data.get(key) == value
    assert response.status_code == HTTPStatus.OK


def test_settings(client):
    response = client.post('/settings')
    assert response.status_code == 401

    user = user_controller.get_user(1)
    login_user(user)

    form = SettingsForm(prefix='form-settings-')
    file_path = os.path.join(client.application.root_path, 'content', 'test_profile_pic.png')

    with open(file_path, 'rb') as f:
        file_contents = f.read()
        response = client.post(
            '/settings', data={
                'username': 'test_user',
                'email': 'test@gmail.com',
                'full_name': 'Test',
                'password': 'pass',
                'bio': 'user info',
                'profile_pic': (BytesIO(file_contents), 'test_profile_pic.png')
            })

        response_message = json.loads(response.data)
        assert response_message == 'Successfully updated profile'
        assert response.status_code == 200


def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 401

    user = user_controller.get_user(1)
    login_user(user)

    response = client.get('/logout')

    response_message = response.get_data(as_text=True)
    assert response_message == '"You have logged out"'
    assert response.status_code == HTTPStatus.OK


def test_get_user(client):
    response = client.get('/user')
    assert response.status_code == 401

    user = user_controller.get_user(1)
    login_user(user)

    response = client.get('/user')

    expected_data = {
        "bio": "user info",
        "email": "test@gmail.com",
        "full_name": "Test",
        "profile_pic": "http://localhost/test_profile_pic.png",
        "username": "test_user"
    }

    response_data = json.loads(response.data)
    for key, value in expected_data.items():
        assert response_data.get(key) == value
    assert response.status_code == HTTPStatus.OK


def test_delete_user(client):
    response = client.delete('/user/delete')
    assert response.status_code == 401

    user = user_controller.get_user(3)
    login_user(user)

    response = client.delete('/user/delete')

    assert response.status_code == 200
