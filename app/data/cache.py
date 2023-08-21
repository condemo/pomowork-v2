import requests
import os
import json

import config
from data.oauth2 import get_token


CACHE_FILE = config.DATA_DIR + "/data.json"


class CacheHandler:
    def __init__(self):
        self.user_credentials = config.USER_HEADERS
        self.user_credentials["Authorization"] = f"Bearer {get_token()}"

        data_fetch = requests.get(
            config.PROJECTS_BASE_URL, headers=self.user_credentials).json()

        data_dict = {
            "projects": data_fetch
        }
        data_dict["project_list"] = []

        for project in data_dict["projects"]:
            project_list = [project["id"], project["name"]]
            data_dict["project_list"].append(project_list)

        with open(CACHE_FILE, "w") as file:
            json.dump(data_dict, file, indent=2)

        os.chmod(CACHE_FILE, 0o600)

    @staticmethod
    def get_project_list() -> list[tuple[int, str]]:
        with open(CACHE_FILE, "r") as file:
            data = json.load(file)

        project_list = [tuple(project) for project in data["project_list"]]
        del data

        return project_list

    @staticmethod
    def get_card_list(id: int) -> list[dict]:
        with open(CACHE_FILE, "r") as file:
            data = json.load(file)

        for project in data["projects"]:
            for card in project["cards"]:
                if card["project_id"] == id:
                    del data
                    return project["cards"]
        del data
