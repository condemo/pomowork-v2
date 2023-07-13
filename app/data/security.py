import os
from cryptography.fernet import Fernet
from config import DATA_DIR


def create_key():
    key = Fernet.generate_key()
    with open(DATA_DIR + "/.key", "wb") as file:
        file.write(key)

    os.chmod(DATA_DIR + "/.key", 0o600)

    return key


def read_key() -> str:
    try:
        with open(DATA_DIR + "/.key", "rb") as file:
            key = file.read()

            return key

    except FileNotFoundError:
        key = create_key()

        return key


def encrypt_token_file() -> None:
    key = read_key()

    f = Fernet(key)

    with open(DATA_DIR + "/.token", "rb") as file:
        original = file.read()

    encrypted = f.encrypt(original)

    with open(DATA_DIR + "/.token", "wb") as file:
        file.write(encrypted)

    os.chmod(DATA_DIR + "/.token", 0o600)


def decrypt_token_file():
    key = read_key()

    f = Fernet(key)

    with open(DATA_DIR + "/.token", "rb") as file:
        encrypted = file.read()

    decrypted = f.decrypt(encrypted)

    return decrypted
