import customtkinter as ctk

from utils.auth import login_handler
from data.oauth2 import save_jwt, save_refresh_token
from config.theme import Colors


class LoginView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, fg_color=Colors.PRIMARY)
        self.pack_propagate(False)

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.main_frame = MainFrame(self)
        self.signup_btn = ctk.CTkButton(
            self, text="Signup", fg_color="transparent",
            text_color="#719CD6", font=("Roboto", 16),
            command=self.go_signup
        )

    def load_widgets(self) -> None:
        self.signup_btn.place(
            anchor="ne", relx=1, rely=0.01)
        self.main_frame.show()

    def show(self) -> None:
        self.pack(expand=True, fill="both")

    def remove(self) -> None:
        self.pack_forget()

    def go_signup(self) -> None:
        self.master.view_controller.change_view("signup", self.master)

    def go_main(self) -> None:
        self.master.view_controller.change_view("main", self.master)


class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master=master, width=400, height=400, fg_color=Colors.BG_SECOND,
            border_width=5, corner_radius=15, border_color=Colors.PRIMARY_DARK)
        self.pack_propagate(False)

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.title = ctk.CTkLabel(self, text="Login", font=("Roboto", 30))
        self.form_frame = FormFrame(self)

    def load_widgets(self) -> None:
        self.title.pack(padx=15, pady=20)
        self.form_frame.show()

    def show(self) -> None:
        self.pack(expand=True)

    def go_main(self) -> None:
        self.master.go_main()


class FormFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, fg_color="transparent")

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.username_entry = ctk.CTkEntry(
            self, placeholder_text="Username", height=40,
            fg_color=Colors.BG_SECOND)
        self.password_entry = ctk.CTkEntry(
            self, placeholder_text="Password", height=40,
            show="*", fg_color=Colors.BG_SECOND)

        self.password_entry.bind("<KeyRelease-Return>", self.send_data)

        self.login_btn = ctk.CTkButton(
            self, text="Ingresar", height=40,
            fg_color=Colors.PRIMARY, command=self.send_data)

    def load_widgets(self) -> None:
        self.username_entry.pack(fill="x", expand=True, pady=3)
        self.password_entry.pack(fill="x", expand=True, pady=3)

        self.login_btn.pack(fill="x", expand=True, pady=3)

    def show(self) -> None:
        self.pack(expand=True, padx=15, fill="x")

    def go_main(self) -> None:
        self.master.go_main()

    def reset_values(self) -> None:
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.username_entry.focus()

    def send_data(self, event=None) -> None:
        login_try = login_handler(self.username_entry.get(), self.password_entry.get())
        if not login_try:
            self.reset_values()
        else:
            token = login_try["access_token"]
            refresh_token = login_try["refresh_token"]
            save_jwt(token)
            save_refresh_token(refresh_token)
            self.go_main()
