import requests
import os
import json
from datetime import date

import config
from lib.models import Card, Project
from data.datasend import DataSender
from data.oauth2 import get_token


CACHE_FILE = config.DATA_DIR + "/data.json"


class CacheHandler:
    def __init__(self):
        self.data_fetch()
        self.data_sender = DataSender()
        self.current_project_id = config.user_conf["core"]["last_open_project"]
        self.current_project = self.load_project(self.current_project_id)

    @staticmethod
    def data_fetch() -> None:
        user_credentials = config.USER_HEADERS
        user_credentials["Authorization"] = f"Bearer {get_token()}"

        data_fetch = requests.get(
            config.PROJECTS_BASE_URL, headers=user_credentials).json()

        data_dict = {
            "projects": data_fetch
        }
        data_dict["project_list"] = []

        for project in data_dict["projects"]:
            project_list = [project["id"], project["name"]]
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

    def get_project_list(self) -> list[tuple[int, str]]:
        data = self.read_data_file()

        project_list = [tuple(project) for project in data["project_list"]]
        del data
        project_list.sort(key=lambda e: e[0], reverse=True)

        return project_list

    def get_card_list(self) -> list[Card]:
        if self.current_project:
            if self.current_project.cards:
                self.card_list = [Card(**i) for i in self.current_project.cards]
                self.card_list.sort(key=lambda e: e.id, reverse=True)
                if self.card_list[0].created_at != str(date.today()):
                    self.card_list.insert(0, self.data_sender.create_new_card({
                        "project_id": self.current_project.id,
                        "price_per_hour": self.current_project.price_per_hour,
                        "total_price": 0,
                        "collected": False
                    }))
            else:
                self.card_list: list = []
                self.card_list.insert(0, self.data_sender.create_new_card({
                    "project_id": self.current_project.id,
                    "price_per_hour": self.current_project.price_per_hour,
                    "total_price": 0,
                    "collected": False
                }))

        return self.card_list

    def get_current_project(self) -> Project:
        return self.current_project

    def load_project(self, id: int) -> Project:
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

    def update_card(self, updated_card: Card) -> None:
        card = self.data_sender.update_card(updated_card)
        if card:
            data = self.read_data_file()
            for project in data["projects"]:
                if project["id"] == card.project_id:
                    project["cards"][0] = card.__dict__
                    self.save_data_file(data)
                    return card
