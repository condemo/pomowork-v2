import requests
from lib.models import Card, Project
from data.oauth2 import get_token
from config import CARDS_BASE_URL, USER_HEADERS, PROJECTS_BASE_URL


class DataSender:
    def __init__(self):
        self.user_credentials = USER_HEADERS
        self.user_credentials["Authorization"] = f"Bearer {get_token()}"

    def create_new_card(self, card: dict) -> Card | None:
        data = requests.post(CARDS_BASE_URL, json=card, headers=self.user_credentials)

        match data.status_code:
            case 201:
                new_card = Card(**data.json())
                return new_card
            case 422:
                print(f"Error de validacion: {data.json()['detail']}")
            case 500:
                print("Error desconocido en el servidor")

    def update_card(self, card: Card) -> Card | None:
        card_dict = card.__dict__
        CARD_UPDATE_URL = f"{CARDS_BASE_URL}{card_dict['project_id']}/{card_dict['id']}"
        data = requests.put(CARD_UPDATE_URL, json=card_dict, headers=self.user_credentials)

        if data.status_code == 200:
            updated_card = Card(**data.json())
            return updated_card

        print(f"{data.json()['detail']}")

    def create_project(self, project: dict) -> Project:
        data = requests.post(PROJECTS_BASE_URL, json=project, headers=self.user_credentials)

        if data.status_code == 201:
            new_project = Project(**data.json())
            return new_project

    def update_project(self, project: Project) -> Project:
        project_dict = project.__dict__
        del project_dict["cards"]
        data = requests.put(PROJECTS_BASE_URL, json=project_dict, headers=self.user_credentials)

        if data.status_code == 200:
            updated_project = Project(**data.json())
            return updated_project

        print(f"{data.json()['detail']}")
