import requests
from tkinter.messagebox import showerror

from config import LOGIN_URL


def login_handler(username: str, password: str):
    headers = {"accept": "application/json",
        'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        "username": username,
        "password": password
    }

    response = requests.post(LOGIN_URL, data=data, headers=headers)
    match response.status_code:
        case 403:
            showerror(response.json()["detail"], "User not Found")
            return False

        case 422:
            showerror("Data Error", "Invalid Format")
            return False

        case 200:
            print(response.json())
            return response.json()
