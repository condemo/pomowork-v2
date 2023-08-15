import customtkinter as ctk
from data.cache import ProjectDataHandler
from views.main.frames import ProjectsFrame, CardsFrame, MainFrame
from utils.cards import CardDataHandler


class HomeView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.pack_propagate(False)

        self.data_handler = ProjectDataHandler()
        self.projects_list = self.data_handler.get_projects()
        self.initial_cards_list = self.data_handler.get_project_cards(
            self.projects_list[0].id
        )

        self.card_handler = CardDataHandler(self.initial_cards_list)
        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.projects_frame = ProjectsFrame(self, self.projects_list)
        self.main_frame = MainFrame(self, self.card_handler.get_last_card())
        self.cards_frame = CardsFrame(self, self.initial_cards_list)

    def load_widgets(self) -> None:
        self.projects_frame.show()
        self.main_frame.show()
        self.cards_frame.show()

    def change_active_project(self, id: int) -> None:
        card_list = self.data_handler.get_project_cards(id)
        self.cards_frame.load_new_cards(card_list)
        if card_list:
            self.main_frame.load_new_data(card_list[0])

    def show(self) -> None:
        self.pack(expand=True, fill="both")

    def remove(self) -> None:
        self.pack_forget()
