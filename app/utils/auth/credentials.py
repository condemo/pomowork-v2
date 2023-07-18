import os
import requests

from config import DATA_DIR, USER_HEADERS, SERVICE_URL
from data.oauth2 import get_token
from data.cache import cache_fetch


class JWTChecker:
    def check_credentials(self) -> str:
        if not os.path.isfile(DATA_DIR + "/.token"):
            return "signup"

        else:
            self.token = get_token()
            # TODO: Implementar checkeo de expiración de el token
            USER_HEADERS["Authorization"] = f"Bearer {self.token}"
            response = requests.get(SERVICE_URL, headers=USER_HEADERS)

            if response.status_code == 200:
                cache_fetch()
                return "main"
            else:
                return "login"
