import pytest
import requests
from data import URL, Answers
import helpers
import allure


@allure.suite('Создание пользователя')
class TestCreateUser:

    @allure.title('Проверка успешного создания пользователя')
    @allure.description('Тест создания пользователя')
    def test_create_user(self, unregistered_user):
        payload = unregistered_user
        response = requests.post(URL.REGISTER, data=payload)
        assert response.status_code == 200 and response.json().get('success') == Answers.TRUE

    @allure.title('Проверка ошибки при создании одинаковых пользователей')
    @allure.description('Тест ошибки создания одинаковых пользователей')
    def test_create_same_user(self, unregistered_user):
        payload = unregistered_user
        requests.post(URL.REGISTER, data=payload)
        response_1 = requests.post(URL.REGISTER, data=payload)
        assert response_1.status_code == 403 and response_1.json().get('message') \
               == Answers.DUPLICATE_USER

    @allure.title('Проверка обязательных полей при создании пользователя')
    @allure.description('Тест при отсутствии обязательных полей при создании пользователя')
    @pytest.mark.parametrize('missing_field', ['email', 'password'])
    def test_required_fields(self, missing_field):
        email, password, name = helpers.generate_unregistered_user()
        payload = {
            'email': email,
            'password': password,
            'name': name
        }
        del payload[missing_field]
        response = requests.post(URL.REGISTER, data=payload)
        assert response.status_code == 403 and response.json().get('message') == Answers.REQUIRED_FIELD
