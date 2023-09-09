import customtkinter as ctk
from tkinter import StringVar
from typing import Optional
from data.datahandlers import ProjectDataHandler


class ProjectsFrame(ctk.CTkFrame):
    def __init__(self, master, data_handler: ProjectDataHandler):
        super().__init__(master=master, width=20)
        self.master = master
        self.pack_propagate(False)

        self.data_handler = data_handler
        self.create_window = None

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.burger_btn = ctk.CTkButton(
            self.top_frame, text="III", width=30, height=30, corner_radius=60)

        self.mid_frame = ProjectsCardFrame(self, self.data_handler)

        self.bottom_frame = ctk.CTkFrame(self)
        self.add_btn = ctk.CTkButton(
            self.bottom_frame, text="ADD", command=self.create_project_window
        )

    def load_widgets(self) -> None:
        self.burger_btn.pack(side="right")
        self.top_frame.pack(fill="x", pady=10, padx=5)

        self.mid_frame.show()

        self.add_btn.pack(fill="x")
        self.bottom_frame.pack(fill="x", pady=10, padx=5)

    def change_active_project(self, id: int) -> None:
        self.master.change_active_project(id)

    def switch_projects_state(self, state: bool) -> None:
        self.mid_frame.switch_projects_state(state)

    def create_project_window(self, config: bool = False, id: Optional[int] = None,
                              name: Optional[str] = None) -> None:
        if self.create_window is None or not self.create_window.winfo_exists():
            self.create_window = NewProjectWindow(self, config=config, id=id, name=name)
        else:
            self.create_window.focus()

    def create_project(self, name: str, price: float = 0) -> None:
        new_project = self.data_handler.create_project({
            "name": name,
            "price_per_hour": price
        })
        self.create_window.destroy()
        self.mid_frame.add_project(new_project.id, new_project.name)

    def update_project(self, id: int, name: str, price: float) -> None:
        print(f"Update {id} - {name} - {price}")
        self.create_window.destroy()

    def show(self) -> None:
        self.pack(side="left", expand=True, fill="both")


class ProjectsCardFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, data_handler: ProjectDataHandler):
        super().__init__(master=master, width=20)
        self.master = master

        self.data_handler = data_handler
        self.projects_list = self.data_handler.get_project_list()
        if self.projects_list:
            self.create_widgets()
            self.load_widgets()
        else:
            self.active_project = None

    def create_widgets(self) -> None:
        self.profile_list = [
            ProjectProfileCard(self, id=i[0], name=i[1]) for i in self.projects_list
        ]
        self.active_project = self.profile_list[0]
        self.active_project.configure(
            fg_color="blue"
        )

    def load_widgets(self) -> None:
        [i.show() for i in self.profile_list]

    def add_project(self, id: int, name: str) -> None:
        if self.projects_list:
            [i.pack_forget() for i in self.profile_list]
        else:
            self.profile_list: list = []
            self.projects_list: list = []
        self.projects_list.insert(0, (id, name))
        new_project = ProjectProfileCard(self, id=id, name=name)
        self.profile_list.insert(0, new_project)
        [i.show() for i in self.profile_list]

    def change_active_project(self, id: int) -> None:
        self.master.change_active_project(id)
        if self.active_project:
            self.active_project.configure(
                fg_color="orange"
            )
        for p in self.profile_list:
            if p.id == id:
                self.active_project = p
                p.configure(
                    fg_color="blue"
                )

    def switch_projects_state(self, state: bool) -> None:
        for p in self.profile_list:
            p.switch_state(state)

    def show(self) -> None:
        self.pack(expand=True, fill="both")


class ProjectProfileCard(ctk.CTkFrame):
    def __init__(self, master, id: int, name: str):
        super().__init__(
            master=master, fg_color="orange", corner_radius=5,
            border_width=3, border_color="red", height=50, cursor="hand2")
        self.grid_propagate(False)
        self.master = master
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
        self.config_btn = ctk.CTkButton(
            self, text="C", fg_color="brown",
            command=lambda: self.master.master.create_project_window(
                config=True, id=self.id, name=self.name))

        self.switch_state(True)

    def load_widgets(self) -> None:
        self.name_label.grid(
            column=0, row=0, rowspan=2, sticky="nswe", padx=5, pady=5)
        self.config_btn.grid(column=1, row=0, rowspan=2, padx=5)

    def switch_state(self, state: bool) -> None:
        if state:
            self.name_label.bind("<Button-1>", self.clicked)
        else:
            self.name_label.unbind("<Button-1>")

    def show(self) -> None:
        self.pack(fill="x", pady=5)

    def clicked(self, event) -> None:
        self.master.change_active_project(self.id)


class NewProjectWindow(ctk.CTkToplevel):
    def __init__(self, master, config: bool, id: Optional[int] = None,
                 name: Optional[str] = None):
        super().__init__(master=master)
        self.master = master
        self.geometry("400x150")
        self.title("Crea un Proyecto")
        self.columnconfigure((0, 1, 2), weight=1, uniform="a")
        self.rowconfigure((0, 1, 2), weight=1, uniform="a")
        self.config_mode = config

        self.name_label = ctk.CTkLabel(
            self, text="Nombre:", font=("Roboto", 22))
        self.price_label = ctk.CTkLabel(
            self, text="€/h", font=("Roboto", 22), anchor="w")
        self.name_entry = ctk.CTkEntry(
            self, width=200, height=50, validate="key",
            validatecommand=(self.master.register(self.validate_name), "%S", "%P"))
        self.price_entry = ctk.CTkEntry(
            self, width=60, height=50, validate="key",
            validatecommand=(self.master.register(self.validate_price), "%S", "%P"))

        self.name_label.grid(column=0, row=0, padx=2, pady=2)
        self.price_label.grid(column=2, row=1, padx=2, pady=2, sticky="w")
        self.name_entry.grid(column=1, row=0, columnspan=2, padx=2, pady=2)
        self.price_entry.grid(column=1, row=1, padx=2, pady=2, sticky="e")

        self.id = id
        self.name = StringVar(self, name)
        if self.config_mode:
            self.load_update_widgets()
        else:
            self.load_create_widgets()

    def load_create_widgets(self) -> None:
        self.create_btn = ctk.CTkButton(
            self, text="Crear", font=("Roboto", 24), command=self.create_project)
        self.create_btn.grid(column=1, row=2, padx=2, pady=6)

    def load_update_widgets(self) -> None:
        self.update_btn = ctk.CTkButton(
            self, text="Modificar", font=("Roboto", 24), command=self.update_project)
        self.remove_btn = ctk.CTkButton(
            self, text="B", font=("Roboto", 24), width=20, fg_color="red")
        self.name_entry.configure(textvariable=self.name)

        self.update_btn.grid(column=1, row=2, padx=2, pady=6)
        self.remove_btn.place(relx=.99, rely=.99, anchor="se")

    @staticmethod
    def validate_name(text: str, new_text: str) -> bool:
        if len(new_text) > 25:
            return False
        if text == " ":
            return True
        return text.isalnum()

    @staticmethod
    def validate_price(text: str, new_text: str) -> bool:
        if len(new_text) > 6:
            return False
        if text == ".":
            return True
        return text.isdecimal()

    def create_project(self) -> None:
        self.master.create_project(self.name_entry.get(), self.price_entry.get())

    def update_project(self) -> None:
        self.master.update_project(self.id, self.name_entry.get(), self.price_entry.get())
