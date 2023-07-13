import base64
from config import DATA_DIR
from data.security import encrypt_token_file, decrypt_token_file


def save_jwt(data: dict) -> None:
    token: str = data["access_token"]
    encoded = base64.b64encode(token.encode())

    with open(DATA_DIR + "/.token", "wb") as file:
        file.write(encoded)

    encrypt_token_file()


def get_token():
    token = decrypt_token_file()

    return base64.b64decode(token).decode("utf-8")
