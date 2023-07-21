import customtkinter as ctk
from views.main.frames import ProjectsFrame, CardsFrame, MainFrame


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
