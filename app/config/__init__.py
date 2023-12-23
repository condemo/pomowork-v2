import os
from typing import Any
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
LICENSE_RESUME = """
GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
"""


class UserConf:
    def __init__(self) -> None:
        if os.path.isfile(f"{CONFIG_FOLDER}/user_conf.toml"):
            self.conf: dict = self.load_config()
        else:
            self.conf: dict = self.create_config()

    def load_config(self) -> dict:
        with open(USER_CONF_FILE, "rt", encoding="utf-8") as file:
            user_conf = tomlkit.load(file)

        return user_conf

    @staticmethod
    def create_config() -> dict:
        initial_config = {
            "core": {"new_version": True, "welcome": True},
            "timers": {
                "pomo_day_count": False,
                "work_timer": 30,
                "short_break_timer": 5,
                "long_break_timer": 15
                },
            "projects": {"initial_mode": "last", "startup_project": False}
        }
        with open(USER_CONF_FILE, "wt", encoding="utf-8") as file:
            tomlkit.dump(initial_config, file)

        return initial_config

    def save(self) -> None:
        with open(USER_CONF_FILE, "wt", encoding="utf-8") as file:
            tomlkit.dump(self.conf, file)

    def get_core_prop(self, prop: str) -> int | bool:
        return self.conf["core"][prop]

    def set_core_prop(self, prop: str, val: Any) -> None:
        self.conf["core"][prop] = val

    def get_timers_prop(self, prop: str) -> int:
        return self.conf["timers"][prop]

    def set_timers_prop(self, prop: str, val: Any) -> None:
        self.conf["timers"][prop] = val

    def get_projects_prop(self, prop: str) -> int | str:
        return self.conf["projects"][prop]

    def set_projects_prop(self, prop: str, val: Any) -> None:
        self.conf["projects"][prop] = val
