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


def load_projects() -> list[Project]:
    projects_list = []
    with open(CACHE_FILE, "r") as file:
        data: dict = json.load(file)

    for i in data:
        project = Project(**i)
        project.cards = []
        for j in i["cards"]:
            card = Card(**j)
            project.cards.append(card)
        projects_list.append(project)

    return projects_list
