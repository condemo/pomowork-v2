import customtkinter as ctk

from views.utils import ViewController
from utils.auth import JWTChecker


class PomoWork(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x800")
        self.title("PomoWork")
        ctk.set_appearance_mode("dark-blue")

        self.credentials_view = JWTChecker()
        self.view_controller = ViewController()

        self.view_controller.change_view(self.credentials_view.check_credentials(), self)

    def go_login_view(self) -> None:
        self.view_controller.change_view("login", self)


if __name__ == "__main__":
    app = PomoWork()
    app.mainloop()
