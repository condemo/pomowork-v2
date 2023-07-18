import requests
import config
import os
from data.oauth2 import get_token
import json


def cache_fetch():
    user_credentials = config.USER_HEADERS
    user_credentials["Authorization"] = f"Bearer {get_token()}"

    data_fetch = requests.get(
        config.PROJECTS_BASE_URL, headers=user_credentials).json()

    with open(config.DATA_DIR + "/data.json", "w") as file:
        json.dump(data_fetch, file, indent=2)

    os.chmod(config.DATA_DIR + "/data.json", 0o600)
