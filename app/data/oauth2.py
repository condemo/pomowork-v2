import base64
from config import DATA_DIR
from data.security import encrypt_token_file, decrypt_token_file


def save_jwt(token: str) -> None:
    encoded = base64.b64encode(token.encode())

    with open(DATA_DIR + "/.token", "wb") as file:
        file.write(encoded)

    encrypt_token_file("token")


def save_refresh_token(token: str) -> None:
    encoded = base64.b64encode(token.encode())

    with open(DATA_DIR + "/.r_token", "wb") as file:
        file.write(encoded)

    encrypt_token_file("r_token")


def get_token(token_type: str):
    token = decrypt_token_file(token_type)

    return base64.b64decode(token).decode("utf-8")


def remove_session() -> None:
    save_jwt("token")
    save_refresh_token("r_token")
