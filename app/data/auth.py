import requests
import json
from config import SIGNUP_URL


def send_signup_request(data: dict) -> dict | Exception:
    data_send = json.dumps(data)
    send = requests.post(url=SIGNUP_URL, data=data_send).json()

    return send