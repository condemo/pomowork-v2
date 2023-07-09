import customtkinter as ctk
# from views.auth import SignupView
from views.auth import LoginView

from views.utils import view_controller


class PomoWork(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self.title("PomoWork")

        # TODO: Borrar al acabar test
        # self.login_view = LoginView(self)
        # self.login_view.show()
        # self.signup_view = SignupView(self)
        # self.signup_view.show()
        view_controller.change_view(LoginView(self))


if __name__ == "__main__":
    app = PomoWork()
    app.mainloop()
