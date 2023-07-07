import customtkinter as ctk
from views.auth import LoginView


class PomoWork(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self.title("PomoWork")

        # TODO: Borrar al acabar test
        self.login_view = LoginView(self)
        self.login_view.show()


if __name__ == "__main__":
    app = PomoWork()
    app.mainloop()
