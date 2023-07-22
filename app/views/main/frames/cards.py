import customtkinter as ctk


class CardsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.pack_propagate(False)

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.top_frame = ctk.CTkFrame(self)
        self.total_time_label = ctk.CTkLabel(
            self.top_frame, text="Horas totales: 12:30", font=("Roboto", 20))

        self.mid_frame = CardListFrame(self)

        self.bottom_frame = ctk.CTkFrame(self)
        self.money_collected_label = ctk.CTkLabel(
            self.bottom_frame, text="Cobrado: 300€", font=("Roboto", 20))
        self.unpaid_money_label = ctk.CTkLabel(
            self.bottom_frame, text="Falta: 400€", font=("Roboto", 20))
        self.total_money_label = ctk.CTkLabel(
            self.bottom_frame, text="Total: 700€", font=("Roboto", 20))

    def load_widgets(self) -> None:
        self.total_time_label.pack()
        self.top_frame.pack(fill="x", pady=5)

        self.mid_frame.show()

        self.money_collected_label.pack(side="left", expand=True)
        self.unpaid_money_label.pack(side="left", expand=True)
        self.total_money_label.pack(side="left", expand=True)
        self.bottom_frame.pack(fill="x")

    def show(self) -> None:
        self.pack(side="left", expand=True, fill="both")


class CardListFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master=master)

        self.load_data()
        self.create_widgets()
        self.load_widgets()

    def load_data(self) -> None:
        pass

    def create_widgets(self) -> None:
        pass

    def load_widgets(self) -> None:
        pass

    def show(self) -> None:
        self.pack(expand=True, fill="both")
