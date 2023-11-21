import customtkinter as ctk

from utils.auth import signup_handler
from config.theme import Colors


class SignupView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, fg_color=Colors.PRIMARY)
        self.pack_propagate(False)

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.main_frame = MainFrame(self)
        self.login_btn = ctk.CTkButton(
            self, text="Login", fg_color="transparent",
            text_color="#719CD6", font=("Roboto", 16),
            command=self.go_login
        )

    def load_widgets(self) -> None:
        self.login_btn.place(anchor="ne", relx=1, rely=0.01)
        self.main_frame.show()

    def show(self):
        self.pack(expand=True, fill="both")

    def remove(self) -> None:
        self.pack_forget()

    def go_login(self) -> None:
        self.master.view_controller.change_view("login", self.master)


class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master=master, width=400, height=400, fg_color=Colors.BG_SECOND,
            border_width=5, border_color=Colors.PRIMARY_DARK, corner_radius=15)
        self.pack_propagate(False)

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.title = ctk.CTkLabel(self, text="Signup", font=("Roboto", 30))
        self.form_frame = FormFrame(self)

    def load_widgets(self) -> None:
        self.title.pack(padx=15, pady=20)
        self.form_frame.show()

    def show(self) -> None:
        self.pack(expand=True)

    def go_login(self) -> None:
        self.master.go_login()


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
            fg_color=Colors.BG_SECOND, show="*")
        self.password_repeat_entry = ctk.CTkEntry(
            self, placeholder_text="Repite Password", height=40,
            fg_color=Colors.BG_SECOND, show="*")
        self.email_entry = ctk.CTkEntry(
            self, placeholder_text="Email: example@example.com",
            fg_color=Colors.BG_SECOND, height=40)

        self.email_entry.bind("<KeyRelease-Return>", self.send_data)

        self.signup_btn = ctk.CTkButton(
            self, text="Crear Cuenta", height=40,
            fg_color=Colors.PRIMARY, command=self.send_data)

    def load_widgets(self) -> None:
        self.username_entry.pack(fill="x", expand=True, pady=3)
        self.password_entry.pack(fill="x", expand=True, pady=3)
        self.password_repeat_entry.pack(fill="x", expand=True, pady=3)
        self.email_entry.pack(fill="x", expand=True, pady=3)
        self.signup_btn.pack(fill="x", expand=True, pady=3)

    def show(self) -> None:
        self.pack(expand=True, padx=15, fill="x")

    def reset_values(self) -> None:
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.password_repeat_entry.delete(0, "end")
        self.email_entry.delete(0, "end")

        self.username_entry.focus()

    def send_data(self, event=None) -> None:
        signup = signup_handler(
            self.username_entry.get(),
            self.password_entry.get(),
            self.password_repeat_entry.get(),
            self.email_entry.get(),
        )
        if not signup:
            self.reset_values()
        else:
            self.master.go_login()
