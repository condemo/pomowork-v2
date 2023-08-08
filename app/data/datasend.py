import requests
from lib.models import Card
from data.oauth2 import get_token
from config import CARDS_BASE_URL, USER_HEADERS


def create_new_card(card: dict) -> Card | None:
    user_credentials = USER_HEADERS
    user_credentials["Authorization"] = f"Bearer {get_token()}"

    data = requests.post(CARDS_BASE_URL, json=card, headers=user_credentials)

    match data.status_code:
        case 201:
            new_card = Card(**data.json())
            return new_card
        case 422:
            print(f"Error de validacion: {data.json()['detail']}")
        case 500:
            print("Error desconocido en el servidor")
