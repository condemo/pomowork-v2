from re import fullmatch
from data.auth import send_signup_request

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def signup_handler(username: str, password: str, repeated_password: str, email: str):
    # TODO: Mejorar la gestion de errores coordinando con send_signup_request
    if password != repeated_password:
        return "Passwords do not match"

    if not fullmatch(regex, email):
        return "Invalid email"

    data: dict = {
        "username": username,
        "password": password,
        "email": email
    }

    response = send_signup_request(data)
    print(response)
