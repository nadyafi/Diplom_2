import requests
from data import URL, Answers
import allure


def valid_hash():
    payload = {
        "ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6c"]
    }
    return payload


@allure.suite('Создание заказа')
class TestCreateOrder:

    @allure.title('Проверка успешного создания заказа  с авторизацией')
    @allure.description('Тест успешного создания заказа с авторизацией')
    def test_create_order_with_auth(self, registered_user):
        payload_1 = registered_user
        requests.post(URL.LOGIN, data=payload_1)
        payload_2 = valid_hash()
        response = requests.post(URL.ORDER, data=payload_2)
        assert response.status_code == 200 and response.json().get('success') == Answers.TRUE

    #Тест падает, это корректный результат. По документации только авторизованный юзер может оформить заказ
    @allure.title('Проверка создания заказа без авторизации')
    @allure.description('Тест создания заказа без авторизации')
    def test_create_order_without_auth(self):
        payload = valid_hash()
        response = requests.post(URL.ORDER, data=payload)
        assert response.status_code == 401 and response.json().get('success') == Answers.UNAUTHORISED

    @allure.title('Проверка неуспешного создания заказа без ингредиентов')
    @allure.description('Тест неуспешного создания заказа без ингредиентов')
    def test_create_order_without_ingredients(self):
        response = requests.post(URL.ORDER)
        assert response.status_code == 400 and response.json().get('message') == Answers.NO_INGREDIENTS

    @allure.title('Проверка неуспешного создания заказа с неверным хешем ингредиентов')
    @allure.description('Тест неуспешного создания заказа с неверным хешем ингредиентов')
    def test_create_order_invalid_hash(self):
        payload = valid_hash()
        payload['ingredients'] += '1'
        response = requests.post(URL.ORDER, data=payload)
        assert response.status_code == 500
