import customtkinter as ctk
from data.cache import load_projects


class HomeView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.pack_propagate(False)

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.projects_frame = ProjectsFrame(self)
        self.main_frame = MainFrame(self)
        self.cards_frame = CardsFrame(self)

    def load_widgets(self) -> None:
        self.projects_frame.show()
        self.main_frame.show()
        self.cards_frame.show()

    def show(self) -> None:
        self.pack(expand=True, fill="both")

    def remove(self) -> None:
        self.pack_forget()


class ProjectsFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(
            master=master, width=100)
        # self.pack_propagate(False)

        self.load_data()
        self.create_widgets()
        self.load_widgets()

    def load_data(self) -> None:
        self.projects_list = load_projects()

    def create_widgets(self) -> None:
        pass

    def load_widgets(self) -> None:
        pass

    def show(self) -> None:
        self.pack(side="left", expand=True, fill="both")


class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.pack_propagate(False)

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.pomo_frame = PomoFrame(self)
        self.info_frame = InfoFrame(self)

    def load_widgets(self) -> None:
        self.pomo_frame.show()
        self.info_frame.show()

    def show(self) -> None:
        self.pack(
            side="left", expand=True, fill="both", padx=15)


class PomoFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, fg_color="red")
        self.pack_propagate(False)

    def create_widgets(self) -> None:
        pass

    def load_widgets(self) -> None:
        pass

    def show(self) -> None:
        self.pack(expand=True, fill="both", pady=7)


class InfoFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, fg_color="orange")
        self.pack_propagate(False)

    def create_widgets(self) -> None:
        pass

    def load_widgets(self) -> None:
        pass

    def show(self) -> None:
        self.pack(expand=True, fill="both", pady=7)


class CardsFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master=master, fg_color="yellow")
        self.pack_propagate(False)

    def create_widgets(self) -> None:
        pass

    def load_widgets(self) -> None:
        pass

    def show(self) -> None:
        self.pack(side="left", expand=True, fill="both")
