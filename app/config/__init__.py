import os
import sys
import tomlkit

CONFIG_FOLDER = os.path.abspath(os.path.dirname(__file__))
DIST_FOLDER = os.path.abspath(os.path.join(CONFIG_FOLDER, os.pardir))
DATA_FOLDER = os.path.join(DIST_FOLDER, "data")

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    print(DATA_FOLDER)
    if not os.path.isdir(CONFIG_FOLDER):
        os.mkdir(CONFIG_FOLDER)
    if not os.path.isdir(DATA_FOLDER):
        os.mkdir(DATA_FOLDER)
        pass
    DATA_DIR = DATA_FOLDER
else:
    if not os.path.isdir(CONFIG_FOLDER):
        os.mkdir(CONFIG_FOLDER)
    if not os.path.isdir(DATA_FOLDER):
        os.mkdir(DATA_FOLDER)
    CURRENT_DIRECTORY = os.path.abspath(os.path.join(CONFIG_FOLDER, os.pardir))
    CONFIG_FOLDER = CURRENT_DIRECTORY + "/config"
    DATA_DIR = CURRENT_DIRECTORY + "/data"

USER_CONF_FILE = CONFIG_FOLDER + "/user_conf.toml"

# SERVER DATA
SERVICE_URL = "http://127.0.0.1:8000/"
PROJECTS_BASE_URL = SERVICE_URL + "projects/"
CARDS_BASE_URL = SERVICE_URL + "cards/"
LOGIN_URL = SERVICE_URL + "login/"
SIGNUP_URL = SERVICE_URL + "users/"
REFRESH_URL = LOGIN_URL + "refresh/"
USER_HEADERS = {
    "accept": "application/json",
    "Authorization": "",
}
REFRESH_HEADERS = {
    "accept": "application/json",
    "Authorization": "",
}


def load_config() -> dict:
    with open(USER_CONF_FILE, "rt", encoding="utf-8") as file:
        user_conf = tomlkit.load(file)

    return user_conf


def create_config() -> dict:
    initial_config = {
        "core": {"last_open_project": 0},
        "pomo": {
            "pomo_day_count": 0,
            "pomo_timer": .1,
            "short_break": .1,
            "long_break": .1
            }
    }
    with open(USER_CONF_FILE, "wt", encoding="utf-8") as file:
        tomlkit.dump(initial_config, file)

    return initial_config


def save_config(user_conf: dict) -> None:
    with open(USER_CONF_FILE, "wt", encoding="utf-8") as file:
        tomlkit.dump(user_conf, file)


if os.path.isfile(f"{CONFIG_FOLDER}/user_conf.toml"):
    user_conf = load_config()
else:
    user_conf = create_config()
