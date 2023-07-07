import customtkinter as ctk


class LoginView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.pack_propagate(False)

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.main_frame = MainFrame(self)
        self.signup_btn = ctk.CTkButton(
            self, text="Signup", fg_color="transparent", text_color="#719CD6", font=("Roboto", 16)
        )

    def load_widgets(self) -> None:
        self.signup_btn.place(anchor="ne", relx=1, rely=0.01)
        self.main_frame.show()

    def show(self):
        self.pack(expand=True, fill="both")


class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, width=400, height=400, border_width=5, corner_radius=15)
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


class FormFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, fg_color="transparent")
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=1, uniform="a")
        self.rowconfigure(2, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=3, uniform="a")

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.username_label = ctk.CTkLabel(self, text="Username:", font=("Roboto", 18))
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")

        self.password_label = ctk.CTkLabel(self, text="Password:", font=("Roboto", 18))
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password")

        self.login_btn = ctk.CTkButton(self, text="Login")

    def load_widgets(self) -> None:
        self.username_label.grid(column=0, row=0, sticky="w", pady=10)
        self.username_entry.grid(column=1, row=0, sticky="we", padx=7, pady=10)

        self.password_label.grid(column=0, row=1, sticky="w")
        self.password_entry.grid(column=1, row=1, sticky="we", padx=7)

        self.login_btn.grid(row=2, column=0, columnspan=2)

    def show(self) -> None:
        self.pack(expand=True, padx=15)
