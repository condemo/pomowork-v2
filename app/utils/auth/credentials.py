import os
import requests
from tkinter.messagebox import showerror

from config import DATA_DIR, USER_HEADERS, SERVICE_URL
from data.oauth2 import get_token


class JWTChecker:
    def check_credentials(self) -> str:
        if not os.path.isfile(DATA_DIR + "/.token"):
            return "signup"

        else:
            self.token = get_token()

            USER_HEADERS["Authorization"] = f"Bearer {self.token}"
            try:
                response = requests.get(SERVICE_URL, headers=USER_HEADERS)
            except requests.exceptions.ConnectionError:
                showerror(
                    "Error de Conexión",
                    "Ha sido imposible conectarse al servidor"
                )
                exit()

            if response.status_code == 200:
                return "main"
            else:
                return "login"
