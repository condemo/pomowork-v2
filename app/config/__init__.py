import os
import tomli
import tomli_w


def load_config():
    with open(USER_CONF_FILE, "rb") as file:
        user_conf = tomli.load(file)

    print(user_conf["core"]["last_open_project"])


def create_config():
    # TODO: Completar la implementació
    initial_config = {
        "core": {"last_open_project": 0}
    }
    with open(USER_CONF_FILE, "wb") as file:
        tomli_w.dump(initial_config, file)

    user_conf = initial_config
    print(user_conf["core"]["last_open_project"])


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

if os.path.isfile(f"{CONFIG_FOLDER}/user_conf.toml"):
    load_config()
else:
    create_config()
