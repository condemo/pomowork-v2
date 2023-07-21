import customtkinter as ctk


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
