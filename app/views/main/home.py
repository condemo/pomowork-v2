import customtkinter as ctk
from data.cache import load_projects


class HomeView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.pack_propagate(False)

        self.load_data()
        self.create_widgets()
        self.load_widgets()

    def load_data(self) -> None:
        self.projects_list = load_projects()

    def create_widgets(self) -> None:
        self.title = ctk.CTkLabel(self, text="HOME VIEW", font=("Roboto", 24))

    def load_widgets(self) -> None:
        self.title.pack()

    def show(self) -> None:
        self.pack(expand=True, fill="both")

    def remove(self) -> None:
        self.pack_forget()
