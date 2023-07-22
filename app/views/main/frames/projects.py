import customtkinter as ctk
from data.cache import load_projects


class ProjectsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, width=20)
        self.pack_propagate(False)

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.burger_btn = ctk.CTkButton(
            self.top_frame, text="III", width=30, height=30, corner_radius=60)

        self.mid_frame = ProjectsCardFrame(self)

        self.bottom_frame = ctk.CTkFrame(self)
        self.add_btn = ctk.CTkButton(self.bottom_frame, text="ADD")

    def load_widgets(self) -> None:
        self.burger_btn.pack(side="right")
        self.top_frame.pack(fill="x", pady=10, padx=5)

        self.mid_frame.show()

        self.add_btn.pack(fill="x")
        self.bottom_frame.pack(fill="x", pady=10, padx=5)

    def show(self) -> None:
        self.pack(side="left", expand=True, fill="both")


class ProjectsCardFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master=master, width=20)

        self.load_data()
        self.create_widgets()
        self.load_widgets()

    def load_data(self) -> None:
        self.projects_list = load_projects()

    def create_widgets(self) -> None:
        self.profile_list = [ProjectProfileCard(self, i.id, i.name) for i in self.projects_list]

    def load_widgets(self) -> None:
        [i.show() for i in self.profile_list]

    def show(self) -> None:
        self.pack(expand=True, fill="both")


class ProjectProfileCard(ctk.CTkFrame):
    def __init__(self, master, id: int, name: str):
        super().__init__(
            master=master, fg_color="orange", corner_radius=5,
            border_width=3, border_color="red", height=50)
        self.grid_propagate(False)
        self.columnconfigure(0, weight=6, uniform="a")
        self.columnconfigure(1, weight=1, uniform="a")
        self.rowconfigure((0, 1), weight=1, uniform="a")

        self.id = id
        self.name = name

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.name_label = ctk.CTkLabel(
            self, text=self.name, font=("Roboto", 18), bg_color="transparent")
        self.config_btn = ctk.CTkButton(self, text="C", fg_color="brown")

    def load_widgets(self) -> None:
        self.name_label.grid(
            column=0, row=0, rowspan=2, sticky="nswe", padx=5, pady=5)
        self.config_btn.grid(column=1, row=0, rowspan=2, padx=5)

    def show(self) -> None:
        self.pack(fill="x", pady=5)