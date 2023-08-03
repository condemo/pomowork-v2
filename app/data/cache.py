import requests
import os
import json

import config
from lib.models import Project, Card
from data.oauth2 import get_token


CACHE_FILE = config.DATA_DIR + "/data.json"


def cache_fetch():
    user_credentials = config.USER_HEADERS
    user_credentials["Authorization"] = f"Bearer {get_token()}"

    data_fetch = requests.get(
        config.PROJECTS_BASE_URL, headers=user_credentials).json()

    with open(CACHE_FILE, "w") as file:
        json.dump(data_fetch, file, indent=2)

    os.chmod(CACHE_FILE, 0o600)


class ProjectDataHandler:
    def __init__(self):

        self.active_project: int
        self.projects_list = []

        with open(CACHE_FILE, "r") as file:
            data: dict = json.load(file)

        for i in data:
            project = Project(**i)
            project.cards = []
            for j in i["cards"]:
                card = Card(**j)
                project.cards.append(card)
            project.cards.sort(key=lambda x: x.created_at, reverse=True)
            self.projects_list.append(project)

    def get_projects(self) -> list[Project]:
        return self.projects_list

    def get_project_cards(self, id: int) -> list[Card]:
        for project in self.projects_list:
            if project.id == id:
                self.active_project = project
                return project.cards
