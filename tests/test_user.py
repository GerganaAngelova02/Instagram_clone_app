import json

import pytest
from http import HTTPStatus
from form.user_register_form import RegistrationForm

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.app_context():
        with app.test_client() as client:
            yield client


def test_index(client):
    response = client.get('/')
    assert b'GerriGram' in response.data


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
        assert b'The username is already taken' in response.data or b'The email is already registered' in response.data
        return
    response_data = json.loads(response.data)
    for key, value in expected_data.items():
        assert response_data.get(key) == value
    assert response.status_code == HTTPStatus.OK
