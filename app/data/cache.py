import requests
import os
import json
from datetime import date
from tkinter.messagebox import showerror

import config
from lib.models import Card, Project
from data.datasend import DataSender
from data.oauth2 import get_token


CACHE_FILE = config.DATA_DIR + "/data.json"
ITEM_FILE = config.DATA_DIR + "/item.json"


class CacheHandler:
    def __init__(self, view):
        self.data_sender = DataSender(view)
        self.check_pending_com()
        self.data_fetch()
        if config.user_conf["core"]["last_open_project"]:
            self.current_project_id = config.user_conf["core"]["last_open_project"]
            self.current_project = self.load_project_by_id(self.current_project_id)
        else:
            self.current_project_id = None
            self.current_project = None

    def check_pending_com(self):
        if os.path.isfile(ITEM_FILE):
            print("ItemFile Exists")
            with open(ITEM_FILE, "r") as file:
                item = json.load(file)
            match item["type"]:
                case "project":
                    match item["mode"]:
                        case "post":
                            self.data_sender.create_project(item["info"])
                        case "put":
                            self.data_sender.update_project(item["info"])
                        case "delete":
                            self.data_sender.remove_project_by_id(item["info"]["id"])
                case "card":
                    match item["mode"]:
                        case "post":
                            self.data_sender.create_new_card(item["info"])
                        case "put":
                            print("Actualizando Tarjeta")
                            self.data_sender.update_card(item["info"])
            os.remove(ITEM_FILE)
            print("Item file removed")

    @staticmethod
    def data_fetch() -> None:
        user_credentials = config.USER_HEADERS
        user_credentials["Authorization"] = f"Bearer {get_token('token')}"

        try:
            data_fetch = requests.get(
                config.PROJECTS_BASE_URL, headers=user_credentials).json()
        except requests.exceptions.ConnectionError:
            showerror(
                "Error de Conexión",
                "Ha sido imposible conectar con el servidor"
            )
            exit()

        data_dict = {
            "projects": data_fetch
        }
        data_dict["project_list"] = []

        for project in data_dict["projects"]:
            project_list = [project["id"], project["name"], project["price_per_hour"]]
            data_dict["project_list"].append(project_list)

        if os.path.isfile(CACHE_FILE):
            with open(CACHE_FILE, "w") as file:
                json.dump(data_dict, file, indent=2)
        else:
            with open(CACHE_FILE, "w") as file:
                json.dump(data_dict, file, indent=2)
            os.chmod(CACHE_FILE, 0o600)

    @staticmethod
    def read_data_file() -> dict:
        with open(CACHE_FILE, 'r') as file:
            data = json.load(file)

        return data

    @staticmethod
    def save_data_file(data: dict) -> None:
        with open(CACHE_FILE, "w") as file:
            json.dump(data, file, indent=2)

    def update_last_open_project(self, id: int) -> None:
        config.user_conf["core"]["last_open_project"] = id
        self.current_project_id = id
        self.current_project = self.load_project_by_id(id)

    def get_project_list(self) -> list[tuple[int, str, float]]:
        data = self.read_data_file()

        project_list = [tuple(project) for project in data["project_list"]]
        del data
        project_list.sort(key=lambda e: e[0], reverse=True)

        return project_list

    def get_current_card_list(self) -> list[Card]:
        if self.current_project:
            if self.current_project.cards:
                self.card_list = [Card(**i) for i in self.current_project.cards]
                self.card_list.sort(key=lambda e: e.id, reverse=True)
                if self.card_list[0].created_at != str(date.today()):
                    self.card_list.insert(0, self.set_card())
            else:
                self.card_list: list = []
                self.card_list.insert(0, self.set_card())
            return self.card_list

    def get_current_project(self) -> Project:
        return self.current_project

    def get_card_list_by_id(self, project_id: int) -> list[Card]:
        data = self.read_data_file()
        card_list: list = []

        for project in data["projects"]:
            if project["id"] == project_id:
                card_dict_list = project["cards"]
                for c in card_dict_list:
                    card = Card(**c)
                    card_list.append(card)
                card_list.sort(key=lambda e: e.created_at, reverse=True)
                return card_list

    def get_last_card_by_id(self, project_id: int) -> Card:
        data = self.read_data_file()

        for project in data["projects"]:
            if project["id"] == project_id:
                card_list: list = project["cards"]
                card_list.sort(key=lambda e: e["created_at"], reverse=True)
                card = Card(**card_list[0])
                return card

    def load_project_by_id(self, id: int) -> Project:
        data = self.read_data_file()

        for project in data["projects"]:
            if project["id"] == id:
                del data
                self.current_project = Project(**project)
                self.current_project_id = self.current_project.id
                return self.current_project
        del data

    def set_project(self, new_project: dict) -> Project:
        project = self.data_sender.create_project(new_project)
        if project:
            data = self.read_data_file()

            data["projects"].append(project.__dict__)
            self.save_data_file(data)
            config.user_conf["core"]["last_open_project"] = project.id
            config.save_config(config.user_conf)
            return project

    def remove_project_by_id(self, id: int) -> bool:
        if self.data_sender.remove_project_by_id(id):
            data = self.read_data_file()
            for project in data["projects"]:
                if project["id"] == id:
                    data["projects"].remove(project)
                    self.save_data_file(data)
                    return True

    def update_project_data(self, updated_project: Project) -> None:
        project = self.data_sender.update_project(updated_project.__dict__)
        if project:
            data = self.read_data_file()

            for p in data["projects"]:
                if p["id"] == project.id:
                    data["projects"].remove(p)
                    data["projects"].append(project.__dict__)
                    self.save_data_file(data)
                    return project

    def update_project(self, id: int, name: str, price: float) -> tuple[int, str, float]:
        data = self.read_data_file()

        for p in data["projects"]:
            if p["id"] == id:
                project = Project(**p)
                project.name = name
                project.price_per_hour = price
                updated_project = self.data_sender.update_project(project.__dict__)
                if updated_project:
                    data["projects"].remove(p)
                    data["projects"].append(updated_project.__dict__)
                    self.save_data_file(data)
                    return (
                        updated_project.id, updated_project.name, updated_project.price_per_hour)

    def set_card(self) -> Card:
        new_card = self.data_sender.create_new_card({
            "project_id": self.current_project.id,
            "price_per_hour": self.current_project.price_per_hour,
            "total_price": 0,
            "collected": False
        })
        if new_card:
            data = self.read_data_file()

            for p in data["projects"]:
                if p["id"] == new_card.project_id:
                    p["cards"].insert(0, new_card.__dict__)
                    self.save_data_file(data)
                    return new_card

    def update_card(self, updated_card: dict) -> Card:
        card_dict = self.data_sender.update_card(updated_card)
        if card_dict:
            card = Card(**card_dict)
            data = self.read_data_file()
            for project in data["projects"]:
                if project["id"] == card.project_id:
                    project_cards: list = project["cards"]
                    for c in project_cards:
                        if c["id"] == card.id:
                            project_cards.remove(c)
                            project_cards.append(card.__dict__)
                            self.save_data_file(data)
                            return card
