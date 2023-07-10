import requests

from config import LOGIN_URL


def login_handler(username: str, password: str):
    headers = {"accept": "application/json",
        'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        "username": username,
        "password": password
    }
    # TODO: Terminar la implementación

    response = requests.post(LOGIN_URL, data=data, headers=headers).json()
    print(response)
