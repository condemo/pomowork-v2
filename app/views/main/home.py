import customtkinter as ctk
from data.datahandlers import ProjectDataHandler
from views.main.frames import ProjectsFrame, CardsFrame, MainFrame


class HomeView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.pack_propagate(False)

        self.data_handler = ProjectDataHandler()
        # self.projects_list = self.data_handler.get_projects()
        # self.initial_cards_list = self.data_handler.get_project_cards(
        #     self.projects_list[0].id
        # )
        #
        # self.card_handler = CardDataHandler(
        #     self, self.data_handler.get_active_project(), self.initial_cards_list)
        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.projects_frame = ProjectsFrame(self, self.data_handler)
        self.main_frame = MainFrame(self, self.data_handler)
        # self.cards_frame = CardsFrame(self, self.initial_cards_list)

    def load_widgets(self) -> None:
        self.projects_frame.show()
        self.main_frame.show()
        # self.cards_frame.show()

    def change_active_project(self, id: int) -> None:
        card_list = self.data_handler.get_project_cards(id)
        self.cards_frame.load_new_cards(card_list)
        if card_list:
            self.card_handler.change_card_list(card_list)
            self.main_frame.load_new_data()

    def update_current_card(self) -> None:
        self.main_frame.load_new_data()

    def show(self) -> None:
        self.pack(expand=True, fill="both")

    def remove(self) -> None:
        self.pack_forget()
