import requests
from lib.models import Card, Project
from data.oauth2 import get_token, save_jwt
from utils import save_pending_com
from config import (
    CARDS_BASE_URL,
    USER_HEADERS,
    PROJECTS_BASE_URL,
    REFRESH_URL,
    REFRESH_HEADERS,
)


class DataSender:
    def __init__(self, view):
        self.view = view
        self.user_credentials = USER_HEADERS
        self.refresh_credentials = REFRESH_HEADERS

        self.user_credentials["Authorization"] = f"Bearer {get_token('token')}"
        self.refresh_credentials["Authorization"] = f"Bearer {get_token('r_token')}"

    def reload_user_crendentials(self) -> None:
        self.user_credentials = USER_HEADERS
        self.refresh_credentials = REFRESH_HEADERS

        self.user_credentials["Authorization"] = f"Bearer {get_token('token')}"
        self.refresh_credentials["Authorization"] = f"Bearer {get_token('r_token')}"

    def create_new_card(self, card: dict) -> Card | None:
        data = requests.post(CARDS_BASE_URL, json=card, headers=self.user_credentials)

        match data.status_code:
            case 201:
                new_card = Card(**data.json())
                return new_card
            case 410:
                req = requests.post(REFRESH_URL, headers=self.refresh_credentials)
                if req.status_code == 200:
                    save_jwt(req.json()["access_token"])
                    self.reload_user_crendentials()
                    return self.create_new_card(card)
                else:
                    save_pending_com("card", "post", card.__dict__)
                    self.view.winfo_toplevel().go_login_view()
            case 422:
                print(f"Error de validacion: {data.json()['detail']}")
            case 500:
                print("Error desconocido en el servidor")

    def update_card(self, card: dict) -> Card | None:
        CARD_UPDATE_URL = f"{CARDS_BASE_URL}{card['project_id']}/{card['id']}"
        data = requests.put(CARD_UPDATE_URL, json=card, headers=self.user_credentials)

        if data.status_code == 200:
            return data.json()
        if data.status_code == 410:
            req = requests.post(REFRESH_URL, headers=self.refresh_credentials)
            if req.status_code == 200:
                save_jwt(req.json()["access_token"])
                self.reload_user_crendentials()
                return self.update_card(card)
            else:
                save_pending_com("card", "put", card)
                self.view.winfo_toplevel().go_login_view()
            print(req.json())

        print(f"{data.json()['detail']}")

    def create_project(self, project: dict) -> Project:
        data = requests.post(PROJECTS_BASE_URL, json=project, headers=self.user_credentials)

        if data.status_code == 201:
            new_project = Project(**data.json())
            return new_project
        if data.status_code == 410:
            req = requests.post(REFRESH_URL, headers=self.refresh_credentials)
            if req.status_code == 200:
                save_jwt(req.json()["access_token"])
                self.reload_user_crendentials()
                return self.create_project(project)
            else:
                save_pending_com("project", "post", project.__dict__)
                self.view.winfo_toplevel().go_login_view()
            print(req.json())

    def update_project(self, project: dict) -> Project:
        if "cards" in project:
            del project["cards"]
        data = requests.put(PROJECTS_BASE_URL, json=project, headers=self.user_credentials)

        if data.status_code == 200:
            updated_project = Project(**data.json())
            return updated_project
        if data.status_code == 410:
            req = requests.post(REFRESH_URL, headers=self.refresh_credentials)
            if req.status_code == 200:
                save_jwt(req.json()["access_token"])
                self.reload_user_crendentials()
                return self.update_project(project)
            else:
                save_pending_com("project", "put", project)
                self.view.winfo_toplevel().go_login_view()
            print(req.json())

        print(f"{data.json()['detail']}")

    def remove_project_by_id(self, id: int) -> bool:
        data = requests.delete(f"{PROJECTS_BASE_URL}{id}", headers=self.user_credentials)

        if data.status_code == 204:
            return True
        if data.status_code == 410:
            req = requests.post(REFRESH_URL, headers=self.refresh_credentials)
            if req.status_code == 200:
                save_jwt(req.json()["access_token"])
                self.reload_user_crendentials()
                return self.remove_project_by_id(id)
            else:
                save_pending_com("project", "delete", {"id": id})
                self.view.winfo_toplevel().go_login_view()
            print(req.json())
