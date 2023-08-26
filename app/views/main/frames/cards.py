import customtkinter as ctk
from lib.models import Card
from data.datahandlers import ProjectDataHandler


class CardsFrame(ctk.CTkFrame):
    def __init__(self, master, data_handler: ProjectDataHandler):
        super().__init__(master=master)
        self.pack_propagate(False)

        self.data_handler = data_handler

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.top_frame = ctk.CTkFrame(self)
        self.total_time_label = ctk.CTkLabel(
            self.top_frame, text="12:30 horas en total", font=("Roboto", 20))

        self.mid_frame = CardListFrame(self, self.data_handler)

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

    def load_new_cards(self) -> None:
        self.mid_frame.load_new_cards()

    def update_data(self) -> None:
        self.mid_frame.update_data()

    def show(self) -> None:
        self.pack(side="left", expand=True, fill="both")


class CardListFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, data_handler: ProjectDataHandler):
        super().__init__(master=master)
        self.data_handler = data_handler
        self.card_list = self.data_handler.get_project_cards()

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.card_widget_list = [PomoCard(self, card) for card in self.card_list]

    def load_widgets(self) -> None:
        [card.show() for card in self.card_widget_list]

    def load_new_cards(self) -> None:
        [card.pack_forget() for card in self.card_widget_list]
        self.card_list = self.data_handler.get_project_cards()
        self.create_widgets()
        self.load_widgets()

    def update_data(self) -> None:
        self.card_widget_list[0].update_data(self.data_handler.get_current_card())

    def show(self) -> None:
        self.pack(expand=True, fill="both")


class PomoCard(ctk.CTkFrame):
    def __init__(self, master, card_data: Card):
        super().__init__(master=master, fg_color="#B13F39", height=50)
        self.grid_propagate(False)
        self.columnconfigure(7, weight=2, uniform="a")
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform="a")
        self.rowconfigure((0, 1, 2), weight=1, uniform="a")

        self.card_data = card_data

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.date_label = ctk.CTkLabel(
            self, text=self.card_data.created_at, font=("Roboto", 16))
        self.price_h_label = ctk.CTkLabel(self, text=f"{self.card_data.price_per_hour:.2f}€/h")
        self.pomo_count_label = ctk.CTkLabel(self, text=f"Pomos: {self.card_data.pomo_count}")
        self.total_money_label = ctk.CTkLabel(
            self, text=f"{self.card_data.total_price:.2f}€", font=("Roboto", 14))
        # TODO: Automatizar el texto en caso de que el campo collected sea true o false
        self.check_box = ctk.CTkCheckBox(
            self, text="No cobrado", checkbox_width=20, checkbox_height=20)

    def load_widgets(self) -> None:
        self.date_label.grid(
            column=3, columnspan=2, row=0, sticky="nswe", pady=1)
        self.price_h_label.grid(column=1, row=1, rowspan=2, sticky="nswe")
        self.pomo_count_label.grid(column=3, row=1, rowspan=2, columnspan=2, sticky="nswe")
        self.total_money_label.grid(column=6, row=1, rowspan=2, sticky="nswe")
        self.check_box.grid(
            column=7, row=0, rowspan=3, sticky="e", padx=5)

    def update_data(self, card_data: Card) -> None:
        # TODO: Implementar la actualizacion de la check_box y el price_per_hour en caso de
        # que sea configurado un cambio y la tarjeta no tenga se haya sido actualizada aún
        self.card_data = card_data
        self.pomo_count_label.configure(
            text=f"Pomos: {card_data.pomo_count}"
        )
        self.total_money_label.configure(
            text=f"{self.card_data.total_price:.2f}€"
        )

    def show(self) -> None:
        self.pack(fill="x", pady=4)
