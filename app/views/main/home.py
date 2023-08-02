import customtkinter as ctk
from data.cache import ProjectDataHandler
from views.main.frames import ProjectsFrame, CardsFrame, MainFrame


class HomeView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.pack_propagate(False)

        self.data_handler = ProjectDataHandler()
        self.projects_list = self.data_handler.get_projects()
        self.initial_cards_list = self.data_handler.get_project_cards(
            self.projects_list[0].id
        )

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.projects_frame = ProjectsFrame(self, self.projects_list)
        self.main_frame = MainFrame(self)
        self.cards_frame = CardsFrame(self, self.initial_cards_list)

    def load_widgets(self) -> None:
        self.projects_frame.show()
        self.main_frame.show()
        self.cards_frame.show()

    def show(self) -> None:
        self.pack(expand=True, fill="both")

    def remove(self) -> None:
        self.pack_forget()
