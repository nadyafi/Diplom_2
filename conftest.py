import pytest
import requests

from data import URL
import helpers


@pytest.fixture
def unregistered_user():
    email, password, name = helpers.generate_unregistered_user()
    payload = {
        'email': f'{email}@mail.com',
        'password': password,
        'name': name
    }

    yield payload

    del payload['name']
    response = requests.post(URL.LOGIN, data=payload)
    token = response.json().get("accessToken")
    headers = {"Authorization": token}
    requests.delete(URL.DELETE_USER, headers=headers)

@pytest.fixture
def registered_user():
    email, password, name = helpers.register_new_user_and_return_email_password()
    payload = {
        'email': f'{email}@mail.com',
        'password': password
    }

    yield payload

    response = requests.post(URL.LOGIN, data=payload)
    token = response.json().get("accessToken")
    headers = {"Authorization": token}
    requests.delete(URL.DELETE_USER, headers=headers)

@pytest.fixture
def valid_hash():
    payload = {
        "ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6c"]
    }

    yield payload

@pytest.fixture
def auth_token(registered_user):
    payload = registered_user
    response = requests.post(URL.LOGIN, data=payload)
    assert response.status_code == 200
    token = response.json().get("accessToken")
    assert token is not None, "Access token was not returned in the response"
    yield token
