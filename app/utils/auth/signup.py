import requests
import json
from re import fullmatch

from tkinter.messagebox import showerror

from config import SIGNUP_URL

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def send_signup_request(data: dict) -> dict | Exception:
    data_send = json.dumps(data)
    send = requests.post(url=SIGNUP_URL, data=data_send)

    return send


def signup_handler(username: str, password: str, repeated_password: str, email: str):
    if password != repeated_password:
        showerror("Password Error", "Password does not match")
        return False

    if not fullmatch(regex, email):
        showerror("Email Error", "Invalid email format")
        return False

    data: dict = {
        "username": username,
        "password": password,
        "email": email
    }

    response = send_signup_request(data)

    match response.status_code:
        case 422:
            showerror("Data Error", "Invalid format")
            return False

        case 201:
            print(response.json())
            return True
