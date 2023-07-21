import customtkinter as ctk


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
