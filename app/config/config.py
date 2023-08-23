import os
import tomli


def load_config():
    with open(f"{CONFIG_FOLDER}/user_conf.toml", "rb") as file:
        config = tomli.load(file)

    print(config["core"]["last_open_project"])


CURRENT_DIRECTORY = os.getcwd() + "/app"
DATA_DIR = CURRENT_DIRECTORY + "/data"
CONFIG_FOLDER = CURRENT_DIRECTORY + "/config"

# SERVER DATA
SERVICE_URL = "http://127.0.0.1:8000/"
PROJECTS_BASE_URL = SERVICE_URL + "projects/"
CARDS_BASE_URL = SERVICE_URL + "cards/"
LOGIN_URL = SERVICE_URL + "login"
SIGNUP_URL = SERVICE_URL + "users/"
USER_HEADERS = {
    "accept": "application/json",
    "Authorization": "",
}

load_config()
