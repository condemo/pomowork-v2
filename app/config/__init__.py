import os
import tomlkit


CURRENT_DIRECTORY = os.getcwd() + "/app"
DATA_DIR = CURRENT_DIRECTORY + "/data"
CONFIG_FOLDER = CURRENT_DIRECTORY + "/config"
USER_CONF_FILE = CONFIG_FOLDER + "/user_conf.toml"

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


def load_config() -> dict:
    with open(USER_CONF_FILE, "rt", encoding="utf-8") as file:
        user_conf = tomlkit.load(file)

    return user_conf


def create_config() -> dict:
    initial_config = {
        "core": {"last_open_project": 0}
    }
    with open(USER_CONF_FILE, "wt", encoding="utf-8") as file:
        tomlkit.dump(initial_config, file)

    return initial_config


if os.path.isfile(f"{CONFIG_FOLDER}/user_conf.toml"):
    user_conf = load_config()
else:
    user_conf = create_config()
