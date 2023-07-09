import requests
import json
from re import fullmatch

from config import SIGNUP_URL

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def send_signup_request(data: dict) -> dict | Exception:
    # TODO: Completar la gestion de errores
    data_send = json.dumps(data)
    send = requests.post(url=SIGNUP_URL, data=data_send).json()

    return send


def signup_handler(username: str, password: str, repeated_password: str, email: str):
    # TODO: Mejorar la gestion de errores coordinando con send_signup_request
    if password != repeated_password:
        return "Passwords do not match"

    if not fullmatch(regex, email):
        return "Invalid email"

    data: dict = {
        "username": username,
        "password": password,
        "email": email
    }

    response = send_signup_request(data)
    print(response)
