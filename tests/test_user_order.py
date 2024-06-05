import requests

from data import URL, Answers
import allure


@allure.suite('Получение заказов конретного пользователя')
class TestUserOrder:

    @allure.title('Проверка получения заказов конкретного пользователя с авторизацией')
    @allure.description('Тест получения заказов конкретного пользователя с авторизацией')
    def test_user_order_with_auth(self, registered_user, auth_token):
        headers = {"Authorization": auth_token}
        response = requests.get(URL.USER_ORDERS, headers=headers)
        assert response.status_code == 200 and response.json().get('success') == Answers.TRUE

    @allure.title('Проверка неуспешного получения заказов конкретного пользователя без авторизации')
    @allure.description('Тест неуспешного получения заказов конкретного пользователя без авторизации')
    def test_user_order_without_auth(self):
        response = requests.get(URL.USER_ORDERS)
        assert response.status_code == 401 and response.json().get('message') == Answers.UNAUTHORISED
