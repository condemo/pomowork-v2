import customtkinter as ctk
from data.datahandlers import ProjectDataHandler
from views.main.frames import ProjectsFrame, CardsFrame, MainFrame


class HomeView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.pack_propagate(False)

        self.data_handler = ProjectDataHandler(self)
        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.projects_frame = ProjectsFrame(self, self.data_handler)
        self.main_frame = MainFrame(self, self.data_handler)
        self.cards_frame = CardsFrame(self, self.data_handler)

    def load_widgets(self) -> None:
        self.projects_frame.show()
        self.main_frame.show()
        self.cards_frame.show()

    def change_active_project(self, id: int) -> None:
        self.data_handler.change_current_project(id)
        self.main_frame.load_active_project()
        self.cards_frame.load_new_cards()
        self.cards_frame.update_project_data()

    def update_project_data(self) -> None:
        self.cards_frame.update_project_data()

    def update_current_card(self, current_card) -> None:
        self.main_frame.update_data(current_card)
        self.cards_frame.update_card_data(current_card)

    def show(self) -> None:
        self.pack(expand=True, fill="both")

    def remove(self) -> None:
        self.pack_forget()
