import customtkinter as ctk
from tkinter import IntVar
from lib.models import Card
from data.datahandlers import DataController
from config.theme import Colors


class CardsFrame(ctk.CTkFrame):
    def __init__(self, master, data_handler: DataController):
        super().__init__(master=master, fg_color="transparent")
        self.pack_propagate(False)

        self.data_handler = data_handler

        try:
            (self.pending_salary, self.salary_collected, self.total_money) = \
                self.data_handler.get_project_total_info()
            self.total_hours = self.data_handler.get_project_total_hours()
            self.create_widgets()
            self.load_widgets()
        except TypeError:
            pass

    def create_widgets(self) -> None:
        self.top_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        self.total_time_label = ctk.CTkLabel(
            self.top_frame,
            text=f"{self.total_hours[0]:02d}:{self.total_hours[1]:02d} horas en total",
            font=("Roboto", 20))

        self.mid_frame = CardListFrame(self, self.data_handler)

        self.bottom_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        self.unpaid_money_label = ctk.CTkLabel(
            self.bottom_frame, text=f"Not Charged: {self.pending_salary:.2f}€",
            font=("Roboto", 18))
        self.money_collected_label = ctk.CTkLabel(
            self.bottom_frame, text=f"Charged: {self.salary_collected:.2f}€",
            font=("Roboto", 18))
        self.total_money_label = ctk.CTkLabel(
            self.bottom_frame, text=f"Total: {self.total_money:.2f}€", font=("Roboto", 18))

    def load_widgets(self) -> None:
        self.total_time_label.pack()
        self.top_frame.pack(fill="x", pady=5)

        self.mid_frame.show()

        self.unpaid_money_label.pack(side="left", expand=True)
        self.money_collected_label.pack(side="left", expand=True)
        self.total_money_label.pack(side="left", expand=True)
        self.bottom_frame.pack(fill="x", pady=4)

    def update_project_data(self) -> None:
        (
            self.pending_salary,
            self.salary_collected,
            self.total_money
        ) = self.data_handler.get_project_total_info()
        self.money_collected_label.configure(
            text=f"Charged: {self.salary_collected:.2f}€"
        )
        self.unpaid_money_label.configure(
            text=f"Not Charged: {self.pending_salary:.2f}€"
        )
        self.total_money_label.configure(
            text=f"Total: {self.total_money:.2f}€"
        )

    def load_new_cards(self) -> None:
        try:
            self.mid_frame.load_new_cards()
        except AttributeError:
            (self.pending_salary, self.salary_collected, self.total_money) = \
                self.data_handler.get_project_total_info()
            self.create_widgets()
            self.load_widgets()

    def update_card_data(self, current_card) -> None:
        self.mid_frame.update_data(current_card)
        self.total_hours = self.data_handler.get_project_total_hours()
        self.total_time_label.configure(
            text=f"{self.total_hours[0]:02d}:{self.total_hours[1]:02d} hours in total"
        )

    def show(self) -> None:
        self.pack(side="left", expand=True, fill="both", padx=(0, 2))


class CardListFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, data_handler: DataController):
        super().__init__(master=master, fg_color=Colors.TRANSPARENT)
        self.data_handler = data_handler
        self.card_list = self.data_handler.get_project_cards()

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.card_widget_list = [PomoCard(self, card) for card in self.card_list]

    def load_widgets(self) -> None:
        [card.show() for card in self.card_widget_list]
        self.card_widget_list[0].set_current()

    def load_new_cards(self) -> None:
        [card.pack_forget() for card in self.card_widget_list]
        self.card_list = self.data_handler.get_project_cards()
        self.create_widgets()
        self.load_widgets()

    def update_data(self, updated_card) -> None:
        self.card_widget_list[0].update_data(updated_card)

    def change_status(self, id: int, status: bool):
        new_card = self.data_handler.update_card_status(id, status)
        return new_card

    def show(self) -> None:
        self.pack(expand=True, fill="both")


class PomoCard(ctk.CTkFrame):
    def __init__(self, master, card_data: Card):
        super().__init__(master=master, fg_color=Colors.ERROR, height=50)
        self.master = master
        self.grid_propagate(False)
        self.columnconfigure(9, weight=2, uniform="a")
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1, uniform="a")
        self.rowconfigure((0, 1, 2), weight=1, uniform="a")

        self.current = False

        self.id = card_data.id
        self.date = card_data.created_at
        self.project_id = card_data.project_id
        self.pomo_count = card_data.pomo_count
        self.price_h = card_data.price_per_hour
        self.status = card_data.collected
        if self.status:
            self.status_text = "Charged"
            self.check_var = IntVar(self, 1)
        else:
            self.status_text = "Not Charged"
            self.check_var = IntVar(self, 0)
        self.total_price = card_data.total_price

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.date_label = ctk.CTkLabel(
            self, text=self.date, font=("Roboto", 16))
        self.price_h_label = ctk.CTkLabel(self, text=f"{self.price_h:.2f}€/h")
        self.pomo_count_label = ctk.CTkLabel(self, text=f"Pomos: {self.pomo_count}")
        self.total_money_label = ctk.CTkLabel(
            self, text=f"{self.total_price:.2f}€", font=("Roboto", 14))
        self.check_box = ctk.CTkCheckBox(
            self, text=self.status_text, checkbox_width=20, checkbox_height=20,
            command=self.change_status, variable=self.check_var, fg_color=Colors.ERROR,
            hover_color=Colors.BG_CARDS_HOVER
        )
        if self.check_var.get():
            if not self.current:
                self.configure(fg_color=Colors.BG_CARDS)
                self.check_box.configure(
                    fg_color=Colors.BG_CARDS, hover_color=Colors.ERROR_HOVER)

    def load_widgets(self) -> None:
        self.date_label.grid(column=4, columnspan=3, row=0, sticky="nswe", pady=1)
        self.price_h_label.grid(column=1, columnspan=3, row=1, rowspan=4, sticky="nswe")
        self.pomo_count_label.grid(column=4, row=1, rowspan=2, columnspan=3, sticky="nswe")
        self.total_money_label.grid(column=7, columnspan=2, row=1, rowspan=2, sticky="nswe")
        self.check_box.grid(column=8, row=0, columnspan=2, rowspan=4, sticky="e", padx=5)

    def set_current(self) -> None:
        self.current = True
        self.configure(fg_color=Colors.PRIMARY)

    def update_data(self, card_data: Card) -> None:
        self.id = card_data.id
        self.date = card_data.created_at
        self.project_id = card_data.project_id
        self.pomo_count = card_data.pomo_count
        self.price_h = card_data.price_per_hour
        self.status = card_data.collected
        if self.status:
            self.status_text = "Charged"
            if not self.current:
                self.configure(fg_color=Colors.BG_CARDS)
        else:
            self.status_text = "Not Charged"
            if not self.current:
                self.configure(fg_color=Colors.ERROR)
        self.total_price = card_data.total_price

        self.price_h_label.configure(
            text=f"{self.price_h:.2f}€/h"
        )
        self.pomo_count_label.configure(
            text=f"Pomos: {self.pomo_count}"
        )
        self.total_money_label.configure(
            text=f"{self.total_price:.2f}€"
        )
        self.check_box.configure(
            text=self.status_text
        )

    def change_status(self) -> None:
        if self.check_box.get() == 0:
            card_data = self.master.change_status(self.id, False)
            self.check_box.configure(
                fg_color=Colors.ERROR, hover_color=Colors.BG_CARDS_HOVER)
        else:
            card_data = self.master.change_status(self.id, True)
            self.check_box.configure(
                fg_color=Colors.BG_CARDS, hover_color=Colors.ERROR_HOVER)

        self.update_data(card_data)
        self.master.data_handler.update_current_project_data()

    def show(self) -> None:
        self.pack(fill="x", pady=4)
