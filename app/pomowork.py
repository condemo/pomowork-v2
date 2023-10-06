import customtkinter as ctk

from views.utils import ViewController
from utils.auth import JWTChecker

_VERSION = "0.0.1"


class PomoWork(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x800")
        self.title("PomoWork")
        ctk.set_appearance_mode("dark")

        self.credentials_view = JWTChecker()
        self.view_controller = ViewController()

        self.view_controller.change_view(self.credentials_view.check_credentials(), self)


if __name__ == "__main__":
    app = PomoWork()
    app.mainloop()
