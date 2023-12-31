import os
import pathlib
import tomlkit

_VERSION = "0.5.4-alpha"

SYS_CONFIG_DIR = os.path.expanduser("~/.config/")
CONFIG_FOLDER = os.path.join(SYS_CONFIG_DIR, "pomowork")
if not os.path.isdir(CONFIG_FOLDER):
    os.mkdir(CONFIG_FOLDER)

SYS_DATA_FOLDER = os.path.expanduser("~/.local/share/")
DATA_DIR = os.path.join(SYS_DATA_FOLDER, "pomowork")
if not os.path.isdir(DATA_DIR):
    os.mkdir(DATA_DIR)

APP_DIR = pathlib.Path(__file__).parent.parent
ASSETS_DIR = APP_DIR / "assets/"

USER_CONF_FILE = CONFIG_FOLDER + "/user_conf.toml"
# SERVER DATA
SERVICE_URL = "https://pomo-service.fly.dev/"  # Prod
# SERVICE_URL = "http://127.0.0.1:8000/"
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

    if "config" in user_conf:
        pass
    else:
        user_conf.update({"config": {"initial_mode": "last"}})

    if "new_version" in user_conf["core"]:
        pass
    else:
        user_conf["core"].update({"new_version": True})

    return user_conf


def create_config() -> dict:
    initial_config = {
        "core": {"startup_project": False, "new_version": True},
        "pomo": {
            "pomo_day_count": 0,
            "pomo_timer": 30,
            "short_break": 5,
            "long_break": 15
            },
        "config": {
            "initial_mode": "last"
        }
    }
    with open(USER_CONF_FILE, "wt", encoding="utf-8") as file:
        tomlkit.dump(initial_config, file)

    return initial_config


def save_config(user_conf: dict) -> None:
    with open(USER_CONF_FILE, "wt", encoding="utf-8") as file:
        tomlkit.dump(user_conf, file)


if os.path.isfile(f"{CONFIG_FOLDER}/user_conf.toml"):
    user_conf: dict = load_config()
else:
    user_conf: dict = create_config()


LICENSE_RESUME = """
GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
"""
