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
        super().__init__(master=master)
        self.pack_propagate(False)
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                             weight=1, uniform="a")
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7),
                          weight=1, uniform="a")

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.config_btn = ctk.CTkButton(
            self.top_frame, text="C", width=30, height=30, corner_radius=30)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.back_btn = ctk.CTkButton(
            self.main_frame, text="<",
            width=30, height=30, corner_radius=30,
            font=("Roboto", 50), fg_color="transparent")
        self.clock_frame = ClockFrame(self.main_frame)
        self.forward_btn = ctk.CTkButton(
            self.main_frame, text=">", width=30,
            height=30, corner_radius=30,
            font=("Roboto", 50), fg_color="transparent")

    def load_widgets(self) -> None:
        self.config_btn.pack(side="right")
        self.top_frame.pack(fill="x", pady=10, padx=5)

        self.back_btn.pack(side="left")
        self.clock_frame.show()
        self.forward_btn.pack(side="left")
        self.main_frame.pack(fill="both", expand=True, padx=2, pady=2)

    def show(self) -> None:
        self.pack(expand=True, fill="both", pady=7)


class ClockFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.mode_label = ctk.CTkLabel(self, text="Work", font=("Roboto", 45))

        self.main_frame = ctk.CTkFrame(self)
        self.timer = ctk.CTkLabel(
            self.main_frame, text="30:00", font=("Roboto", 100))

        self.control_frame = ctk.CTkFrame(self.main_frame)
        self.pause_btn = ctk.CTkButton(
            self.control_frame, text="II", font=("Roboto", 50), fg_color="transparent")
        self.stop_btn = ctk.CTkButton(
            self.control_frame, text="ST", font=("Roboto", 50), fg_color="transparent")

    def load_widgets(self) -> None:
        self.mode_label.pack()

        self.timer.pack()
        self.main_frame.place(relx=.5, rely=.5, anchor="center")

        self.pause_btn.pack(side="left", padx=10)
        self.stop_btn.pack(side="left", padx=10)
        self.control_frame.pack(fill="x", pady=10)

    def show(self) -> None:
        self.pack(side="left", fill="both", expand=True)


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
