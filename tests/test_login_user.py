import requests
from data import URL, Answers
import pytest
import allure


@allure.suite('Логин пользователя в системе')
class TestLoginUser:
    
    @allure.title('Проверка успешной авторизации пользователя в системе')
    @allure.description('Тест успешной авторизации пользователя в системе')
    def test_login_user(self, registered_user):
        payload = registered_user
        response = requests.post(URL.LOGIN, data=payload)
        assert response.status_code == 200 and response.json().get('success') == Answers.TRUE


    
    @allure.title('Проверка авторизации с некорректными данными')
    @allure.description('Тест авторизации с некорректными данными')
    @pytest.mark.parametrize('invalid_field', ['email', 'password'])
    def test_login_user_with_invalid_field(self, registered_user, invalid_field):
        payload = registered_user.copy()
        payload[invalid_field] += '1'
        response = requests.post(URL.LOGIN, data=payload)
        assert response.status_code == 401 and response.json().get('message') == Answers.INCORRECT
