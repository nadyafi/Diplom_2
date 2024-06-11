import requests
import random
import string
from data import URL


# метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
def generate_random_string(length):
    random_string = ''.join(random.choices(string.ascii_lowercase, k=length))
    return random_string


def register_new_user_and_return_email_password():
    # создаём список, чтобы метод мог его вернуть
    login_pass = []

    email = generate_random_string(10)
    password = generate_random_string(10)
    name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "email": f'{email}@mail.com',
        "password": password,
        "name": name
    }
    response = requests.post(URL.REGISTER, data=payload)

    if response.status_code == 200:
        login_pass.append(email)
        login_pass.append(password)
        login_pass.append(name)

    # возвращаем список
    return login_pass


def generate_unregistered_user():
    user_data = []
    while len(user_data) != 3:
        user_data.append(generate_random_string(8))
    return user_data
