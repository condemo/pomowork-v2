import customtkinter as ctk
from tkinter.messagebox import askokcancel
from CTkToolTip import CTkToolTip
from tkfontawesome import icon_to_image
from typing import Optional
from data.datahandlers import DataController
from utils.infomessage import InfoMessage
from config.theme import Colors


class ProjectsFrame(ctk.CTkFrame):
    def __init__(self, master, data_handler: DataController):
        super().__init__(master=master, fg_color=Colors.BACKGROUND, width=20)
        self.master = master
        self.pack_propagate(False)

        self.data_handler = data_handler
        self.create_window = None

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        # ICON LOAD
        add_icon = icon_to_image("plus", fill="white", scale=0.042)
        # WIDGETS LOAD
        self.top_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        self.project_section_label = ctk.CTkLabel(
            self.top_frame, text="Projects", font=("Roboto", 20))

        self.mid_frame = ProjectsCardFrame(self, self.data_handler)

        self.bottom_frame = ctk.CTkFrame(self)
        self.add_btn = ctk.CTkButton(
            self.bottom_frame, text="", command=self.create_project_window, image=add_icon,
            fg_color=Colors.SECONDARY, bg_color="transparent", hover_color=Colors.SECONDARY_HOVER,
            font=("Roboto", 16), compound="right"
        )

    def load_widgets(self) -> None:
        self.project_section_label.pack()
        self.top_frame.pack(fill="x", pady=4)

        self.mid_frame.show()

        self.add_btn.pack(fill="x")
        self.bottom_frame.pack(fill="x", pady=4)

        CTkToolTip(self.add_btn, message="New Project",
                   corner_radius=20, bg_color=Colors.BG_SECOND)

    def change_active_project(self, id: int) -> None:
        self.master.change_active_project(id)

    def switch_projects_state(self, state: bool) -> None:
        self.mid_frame.switch_projects_state(state)

    def create_project_window(
            self, config: bool = False, id: Optional[int] = None,
            name: Optional[str] = None, price: Optional[float] = None) -> None:
        if self.data_handler.get_ui_status():
            if self.create_window is None or not self.create_window.winfo_exists():
                self.create_window = NewProjectWindow(
                    self, config=config, id=id, name=name, price=price)
            else:
                self.create_window.focus()
        else:
            InfoMessage(self.winfo_toplevel(), mode="info",
                        text="Timer is running")

    def create_project(self, name: str, price: float = 0) -> None:
        new_project = self.data_handler.create_project({
            "name": name,
            "price_per_hour": price
        })
        self.create_window.destroy()
        self.mid_frame.add_project(new_project.id, new_project.name, new_project.price_per_hour)

    def update_project(self, id: int, name: str, price: float) -> None:
        updated_project = self.data_handler.update_project(id, name, price)
        self.mid_frame.update_project_info(updated_project)
        self.create_window.destroy()

    def remove_project(self, id: int) -> None:
        if self.data_handler.remove_project_by_id(id):
            self.create_window.destroy()
            self.mid_frame.remove_project(id)

    def show(self) -> None:
        self.pack(side="left", expand=True, fill="both", padx=(4, 0))


class ProjectsCardFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, data_handler: DataController):
        super().__init__(master=master, fg_color=Colors.TRANSPARENT, width=20)
        self.master = master

        self.data_handler = data_handler
        self.projects_list = self.data_handler.get_project_list()
        self.active_project = None
        if self.projects_list:
            self.startup_project_id = self.data_handler.get_startup_project()
            self.create_widgets()
            self.load_widgets()

    def create_widgets(self) -> None:
        self.profile_list = [
            ProjectProfileCard(self, id=i[0], name=i[1], price=i[2]) for i in self.projects_list
        ]
        if self.startup_project_id:
            if self.profile_list:
                for p in self.profile_list:
                    if p.id == self.startup_project_id:
                        self.active_project = p
            else:
                self.active_project = None
        elif self.profile_list:
            self.active_project = self.profile_list[0]
        else:
            self.active_project = None

        if self.active_project:
            self.active_project.configure(
                fg_color=Colors.PRIMARY,
                border_width=2,
                border_color=Colors.PRIMARY_HOVER,
            )
            self.active_project.config_btn.configure(
                fg_color=Colors.PRIMARY,
                hover_color=Colors.PRIMARY_DARK,
            )

    def load_widgets(self) -> None:
        [i.show() for i in self.profile_list]

    def add_project(self, id: int, name: str, price: float) -> None:
        if self.projects_list:
            [i.pack_forget() for i in self.profile_list]
        else:
            self.profile_list: list = []
            self.projects_list: list = []
        self.projects_list.insert(0, (id, name, price))
        new_project = ProjectProfileCard(self, id=id, name=name, price=price)
        self.profile_list.insert(0, new_project)
        [i.show() for i in self.profile_list]

    def remove_project(self, id: int) -> None:
        for p in self.projects_list:
            if p[0] == id:
                self.projects_list.remove(p)
        for project in self.profile_list:
            if project.id == id:
                self.profile_list.remove(project)
                project.pack_forget()
        self.change_active_project(self.projects_list[0][0])
        self.data_handler.save_new_last_open_project(id=False)

    def change_active_project(self, id: int) -> None:
        self.master.change_active_project(id)
        if self.active_project:
            self.active_project.configure(
                fg_color=Colors.BG_PROJECTS,
                border_width=0,
            )
            self.active_project.config_btn.configure(
                fg_color=Colors.BG_PROJECTS,
                hover_color=Colors.CONFIG_PROJECT,
            )
        for p in self.profile_list:
            if p.id == id:
                self.active_project = p
                p.configure(
                    fg_color=Colors.PRIMARY,
                    border_width=2,
                    border_color=Colors.PRIMARY_HOVER,
                )
                p.config_btn.configure(
                    fg_color=Colors.PRIMARY,
                    hover_color=Colors.PRIMARY_DARK,
                )

    def update_project_info(self, project: tuple[int, str, float]) -> None:
        for p in self.profile_list:
            if p.id == project[0]:
                p.update_data(project)

    def switch_projects_state(self, state: bool) -> None:
        for p in self.profile_list:
            p.switch_state(state)

    def show(self) -> None:
        self.pack(expand=True, fill="both")


class ProjectProfileCard(ctk.CTkFrame):
    def __init__(self, master, id: int, name: str, price: float):
        super().__init__(
            master=master, fg_color=Colors.BG_PROJECTS, corner_radius=5,
            height=50, cursor="hand2")
        self.grid_propagate(False)
        self.master = master
        self.columnconfigure(0, weight=6, uniform="a")
        self.columnconfigure(1, weight=1, uniform="a")
        self.rowconfigure((0, 1), weight=1, uniform="a")

        self.id = id
        self.name = name
        self.price = price

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        # ICONS
        config_icon = icon_to_image("edit", fill=Colors.ERROR_HOVER, scale=0.042)
        # WIDGETS
        self.name_label = ctk.CTkLabel(
            self, text=self.name, font=("Roboto", 18), bg_color="transparent")
        self.config_btn = ctk.CTkButton(
            self, text="", fg_color=Colors.BG_PROJECTS, hover_color=Colors.CONFIG_PROJECT,
            image=config_icon,
            command=lambda: self.master.master.create_project_window(
                config=True, id=self.id, name=self.name, price=self.price))

        self.switch_state(True)

    def load_widgets(self) -> None:
        self.name_label.grid(
            column=0, row=0, rowspan=2, sticky="nswe", padx=5, pady=5)
        self.config_btn.grid(column=1, row=0, rowspan=2, padx=5)

        CTkToolTip(self.config_btn, message="Project Config", bg_color=Colors.BG_SECOND)

    def switch_state(self, state: bool) -> None:
        if state:
            self.name_label.bind("<Button-1>", self.clicked)
        else:
            self.name_label.unbind("<Button-1>")

    def update_data(self, project: tuple[int, str, float]) -> None:
        self.name = project[1]
        self.price = project[2]
        self.name_label.configure(text=f"{self.name}")

    def show(self) -> None:
        self.pack(fill="x", pady=5)

    def clicked(self, event) -> None:
        if self.master.data_handler.get_ui_status():
            self.master.change_active_project(self.id)


class NewProjectWindow(ctk.CTkToplevel):
    def __init__(self, master, config: bool, id: Optional[int] = None,
                 name: Optional[str] = None, price: Optional[float] = None):
        super().__init__(master=master, fg_color=Colors.BACKGROUND)
        self.master = master
        self.geometry("400x150")
        self.title("Create a Project")
        self.columnconfigure((0, 1, 2), weight=1, uniform="a")
        self.rowconfigure((0, 1, 2), weight=1, uniform="a")
        self.config_mode = config

        self.name_label = ctk.CTkLabel(
            self, text="Name:", font=("Roboto", 22))
        self.price_label = ctk.CTkLabel(
            self, text="€/h", font=("Roboto", 22), anchor="w")
        self.name_entry = ctk.CTkEntry(
            self, width=200, height=50, validate="key", fg_color=Colors.BG_SECOND,
            validatecommand=(self.master.register(self.validate_name), "%S", "%P"))
        self.price_entry = ctk.CTkEntry(
            self, width=60, height=50, validate="key", fg_color=Colors.BG_SECOND,
            validatecommand=(self.master.register(self.validate_price), "%S", "%P"))

        self.name_label.grid(column=0, row=0, padx=2, pady=2)
        self.price_label.grid(column=2, row=1, padx=2, pady=2, sticky="w")
        self.name_entry.grid(column=1, row=0, columnspan=2, padx=2, pady=2)
        self.price_entry.grid(column=1, row=1, padx=2, pady=2, sticky="e")

        self.id = id

        if self.id:
            self.name = name
            self.price = str(price)
        else:
            self.name = ""
            self.price = ""

        if self.config_mode:
            self.load_update_widgets()
        else:
            self.load_create_widgets()

    def load_create_widgets(self) -> None:
        create_icon = icon_to_image("save", fill="white", scale=0.042)
        self.create_btn = ctk.CTkButton(
            self, text="Create", font=("Roboto", 24), image=create_icon, compound="right",
            fg_color=Colors.SECONDARY, hover_color=Colors.SECONDARY_HOVER,
            command=self.create_project)
        self.create_btn.grid(column=1, row=2, padx=2, pady=6)

    def load_update_widgets(self) -> None:
        # ICONS
        update_icon = icon_to_image("pencil-alt", fill="white", scale=0.042)
        delete_icon = icon_to_image("trash-alt", fill="white", scale=0.042)
        # WIDGETS
        self.update_btn = ctk.CTkButton(
            self, text="Modify", font=("Roboto", 24), image=update_icon, compound="right",
            fg_color=Colors.SECONDARY, hover_color=Colors.SECONDARY_HOVER,
            command=self.update_project)
        self.remove_btn = ctk.CTkButton(
            self, text="", font=("Roboto", 24), width=20, image=delete_icon, compound="right",
            fg_color=Colors.ERROR, hover_color=Colors.ERROR_HOVER,
            command=self.remove_project)
        self.name_entry.insert(0, self.name)
        # FIX: No funciona este insert por algún motivo
        self.price_entry.insert(0, self.price)

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
        if self.price_entry.get() == "":
            price = 0
        else:
            price = self.price_entry.get()
        self.master.create_project(self.name_entry.get(), float(price))

    def update_project(self) -> None:
        if self.price_entry.get() == "":
            price = self.price
        else:
            price = self.price_entry.get()
        self.master.update_project(self.id, self.name_entry.get(), float(price))

    def remove_project(self) -> None:
        if askokcancel("Delete Project", "You are about to delete a project, are you sure?"):
            self.master.remove_project(self.id)
