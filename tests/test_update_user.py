import pytest
import requests
from data import URL, Answers
import allure
import random


def generate_unique_email():
    email = f'testuser{random.randint(100, 999)}@yandex.ru'
    return email


@allure.suite('Изменение данных пользователя в системе')
class TestUpdateUser:

    @allure.title('Проверка успешного изменения email пользователя в системе')
    @allure.description('Тест успешного изменения email пользователя в системе')
    @pytest.mark.parametrize('new_email', [generate_unique_email()])
    def test_update_user_email(self, auth_token, registered_user, new_email):
        headers = {"Authorization": auth_token}
        response_1 = requests.patch(URL.USER, headers=headers, data={'email':new_email})
        assert response_1.status_code == 200 and response_1.json().get('success') == Answers.TRUE
        response_2 = requests.get(URL.USER, headers=headers)
        assert response_2.status_code == 200
        response_data = response_2.json()
        user_data = response_data.get('user', {})
        assert user_data.get('email') == new_email

    @allure.title('Проверка успешного изменения пароля пользователя в системе')
    @allure.description('Тест успешного изменения пароля пользователя в системе')
    @pytest.mark.parametrize('new_password', ['newpassword_1'])
    def test_update_user_password(self, auth_token, new_password, registered_user):
        headers = {"Authorization": auth_token}
        response_1 = requests.patch(URL.USER, headers=headers, data={'password': new_password})
        assert response_1.status_code == 200
        assert response_1.json().get('success') == Answers.TRUE

    @allure.title('Проверка успешного изменения email и пароля пользователя в системе')
    @allure.description('Тест успешного изменения email и пароля пользователя в системе')
    @pytest.mark.parametrize('new_email, new_password', [(generate_unique_email(), 'newpassword')])
    def test_update_user_email_and_password(self, auth_token, new_email, new_password, registered_user):
        headers = {"Authorization": auth_token}
        response_1 = requests.patch(URL.USER, headers=headers, data={'email': new_email, 'password': new_password})
        assert response_1.status_code == 200
        assert response_1.json().get('success') == Answers.TRUE

        response_2 = requests.get(URL.USER, headers=headers)
        assert response_2.status_code == 200
        response_data = response_2.json()
        user_data = response_data.get('user', {})
        assert user_data.get('email') == new_email

    @allure.title('Проверка неуспешного изменения данных пользователя в системе без авторизации')
    @allure.description('Тест неуспешного изменения данных пользователя в системе без авторизации')
    def test_update_user_without_auth(self):
        response = requests.patch(URL.USER)
        assert response.status_code == 401 and response.json().get('message') == Answers.UNAUTHORISED

    @allure.title('Проверка неуспешного изменения данных пользователя при передаче существующей почты')
    @allure.description('Тест неуспешного изменения данных пользователя при передаче существующей почты')
    def test_unsuccessful_update_user_with_exist_email(self, registered_user, auth_token):
        headers = {"Authorization": auth_token}
        payload = {"email": 'nf7q@yandex.ru'}
        response = requests.patch(URL.USER, headers=headers, json=payload)
        assert response.status_code == 403 and response.json().get('message') == Answers.UPDATE_EXIST_EMAIL
