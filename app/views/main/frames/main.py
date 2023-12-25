from datetime import datetime
import customtkinter as ctk
from CTkToolTip import CTkToolTip
from tkfontawesome import icon_to_image
from data.datahandlers import DataController
from utils.infomessage import InfoMessage
from views.main.configframe import ConfigWindow
from views.timer import ClockFrame
from config.theme import Colors


class MainFrame(ctk.CTkFrame):
    def __init__(self, master, data_handler: DataController):
        super().__init__(master=master, fg_color="transparent")
        self.master = master
        self.pack_propagate(False)

        self.data_handler = data_handler

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.pomo_frame = PomoFrame(self, self.data_handler)
        self.info_frame = InfoFrame(self, self.data_handler)

    def load_widgets(self) -> None:
        self.pomo_frame.show()
        self.info_frame.show()

    def update_data(self, updated_card) -> None:
        self.info_frame.update_data(updated_card)

    def update_title(self) -> None:
        self.pomo_frame.update_title()

    def update_info_buttons(self, count: int) -> None:
        self.info_frame.update_info_buttons(count)

    def load_active_project(self) -> None:
        self.info_frame.load_last_card()
        self.update_title()

    def reload_timers(self, timers: tuple[int]) -> None:
        self.pomo_frame.reload_timers(timers)

    def show(self) -> None:
        self.pack(side="left", expand=True, fill="both", padx=15)


class PomoFrame(ctk.CTkFrame):
    def __init__(self, master, data_handler: DataController):
        super().__init__(master=master, fg_color="transparent")
        self.master = master
        self.pack_propagate(False)
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                             weight=1, uniform="a")
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7),
                          weight=1, uniform="a")

        self.data_handler = data_handler
        self.config_window = None

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        # ICONS
        config_icon = icon_to_image("cog", fill="white", scale=0.042)
        forward_icon = icon_to_image("arrow-right", fill="white", scale=0.06)
        back_icon = icon_to_image("arrow-left", fill="white", scale=0.06)
        # WIDGETS
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.title_label = ctk.CTkLabel(
            self.top_frame, text=f"{self.data_handler.get_current_project_name()}",
            font=("Roboto", 28)
        )
        self.config_btn = ctk.CTkButton(
            self.top_frame, text="", width=25, height=35, corner_radius=30,
            fg_color=Colors.GREY, hover_color=Colors.GREY_HOVER, image=config_icon,
            command=self.create_config_window
        )

        self.main_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        self.back_btn = ctk.CTkButton(
            self.main_frame, text="", width=30, height=30, image=back_icon,
            corner_radius=30, font=("Roboto", 50), fg_color="transparent",
            hover_color=Colors.PRIMARY, border_spacing=6, command=self.back_mode
        )
        self.clock_frame = ClockFrame(self.main_frame, self.data_handler)
        self.forward_btn = ctk.CTkButton(
            self.main_frame, text="", width=30, height=30, image=forward_icon,
            corner_radius=30, font=("Roboto", 50), fg_color="transparent",
            hover_color=Colors.PRIMARY, border_spacing=6, command=self.forward_mode
        )

    def load_widgets(self) -> None:
        self.title_label.pack()
        self.config_btn.pack(side="right")
        self.top_frame.pack(fill="x", pady=10, padx=5)

        self.back_btn.pack(side="left")
        self.clock_frame.show()
        self.forward_btn.pack(side="left")
        self.main_frame.pack(fill="both", expand=True, padx=2, pady=2)

        CTkToolTip(self.config_btn, message="Config", bg_color=Colors.BG_SECOND)
        CTkToolTip(self.forward_btn, message="Next Mode", bg_color=Colors.BG_SECOND)
        CTkToolTip(self.back_btn, message="Previous Mode", bg_color=Colors.BG_SECOND)

    def create_config_window(self) -> None:
        if self.data_handler.get_ui_status():
            if self.config_window is None or not self.config_window.winfo_exists():
                self.config_window = ConfigWindow(self, self.data_handler)
            else:
                self.config_window.focus()
        else:
            InfoMessage(self.winfo_toplevel(), mode="error",
                        text="Timer is running")

    def back_mode(self) -> None:
        if self.data_handler.get_ui_status():
            self.clock_frame.back_mode()
        else:
            InfoMessage(self.winfo_toplevel(), mode="error",
                        text="Timer is running")

    def forward_mode(self) -> None:
        if self.data_handler.get_ui_status():
            self.clock_frame.forward_mode()
        else:
            InfoMessage(self.winfo_toplevel(), mode="error",
                        text="Timer is running")

    def update_title(self) -> None:
        self.title_label.configure(
            text=f"{self.data_handler.get_current_project_name()}"
        )

    def reload_timers(self, timers: tuple[int]) -> None:
        self.clock_frame.reload_timers(timers)

    def show(self) -> None:
        self.pack(expand=True, fill="both", pady=7)


class InfoFrame(ctk.CTkFrame):
    def __init__(self, master, data_handler: DataController):
        super().__init__(
            master=master, fg_color=Colors.BG_SECOND, corner_radius=20,
            border_width=2, border_color=Colors.PRIMARY)
        self.pack_propagate(False)
        self.data_handler = data_handler
        self.last_card = self.data_handler.get_current_card()

        if self.last_card:
            self.check_card_date()
            self.card_hour, self.card_minutes = self.data_handler.get_current_card_total_hours()
        self.pomo_day_count = self.data_handler.get_pomo_day_count()
        self.create_widgets()
        self.load_widgets()

    def check_card_date(self) -> str:
        if self.last_card:
            self.last_card_date = datetime.strptime(
                self.last_card.created_at, "%Y-%m-%d"
            ).strftime("%d/%m/%Y")

    def create_widgets(self) -> None:
        if self.last_card:
            self.top_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
            self.price_h_label = ctk.CTkLabel(
                self.top_frame, text=f"Price/h: {self.last_card.price_per_hour:.2f}€",
                font=("Roboto", 18))
            self.date_label = ctk.CTkLabel(
                self.top_frame, text=f"{self.last_card_date}", font=("Roboto", 30))

            self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.info_container_frame = ctk.CTkFrame(self.main_frame, fg_color=Colors.TRANSPARENT)
            self.pomo_num_label = ctk.CTkLabel(
                self.info_container_frame,
                text=f"Pomodoros: {self.last_card.pomo_count}", font=("Roboto", 50))
            self.total_time_label = ctk.CTkLabel(
                self.info_container_frame,
                text=f"Time Today: {self.card_hour:02d}:{self.card_minutes:02d}h",
                font=("Roboto", 20))

            self.bottom_frame = ctk.CTkFrame(
                self, fg_color=Colors.TRANSPARENT, corner_radius=15, bg_color=Colors.PRIMARY)
            self.total_money_label = ctk.CTkLabel(
                self.bottom_frame, fg_color=Colors.PRIMARY, corner_radius=15,
                bg_color=Colors.PRIMARY,
                text=f"Total Today: {self.last_card.total_price:.2f}€", font=("Roboto", 30))

        self.pomo_day_main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.pomo_day_left_frame = ctk.CTkFrame(
            self.pomo_day_main_frame, fg_color="transparent")
        self.pomo_day_right_frame = ctk.CTkFrame(
            self.pomo_day_main_frame, fg_color="transparent")

        self.radio_btn_list = [ctk.CTkRadioButton(
            self.pomo_day_left_frame, text="", width=10, fg_color=Colors.PRIMARY,
            state="readonly", border_width_checked=10) for i in range(4)]
        [self.radio_btn_list.append(ctk.CTkRadioButton(
            self.pomo_day_right_frame, text="", width=10, fg_color=Colors.PRIMARY,
            state="readonly", border_width_checked=10)) for i in range(4)]

    def load_widgets(self) -> None:
        if self.last_card:
            self.top_frame.pack(pady=4)
            self.price_h_label.pack(side="left", padx=20)
            self.date_label.pack(side="left", padx=20)

            self.pomo_day_main_frame.pack(pady=50)
            self.pomo_day_left_frame.pack(side="left", padx=15)
            self.pomo_day_right_frame.pack(side="left", padx=15)
            [i.pack(side="left") for i in self.radio_btn_list]
            [self.radio_btn_list[i].select() for i in range(self.pomo_day_count)]

            self.pomo_num_label.pack(pady=5)
            self.total_time_label.pack()
            self.info_container_frame.pack(expand=True)
            self.main_frame.pack(expand=True, fill="both", padx=3)

            self.total_money_label.pack(fill="x")
            self.bottom_frame.pack(fill="x", padx=1)

    def load_last_card(self) -> None:
        if self.last_card:
            self.last_card = self.data_handler.get_current_card()
            self.check_card_date()
            self.price_h_label.configure(
                text=f"Price/h: {self.last_card.price_per_hour:.2f}€", font=("Roboto", 18)
            )
            self.date_label.configure(
                text=f"{self.last_card_date}", font=("Roboto", 30)
            )
            self.pomo_num_label.configure(
                text=f"Pomodoros: {self.last_card.pomo_count}", font=("Roboto", 50)
            )
            self.total_time_label.configure(
                text=f"Time Today: {self.card_hour:02d}:{self.card_minutes:02d}h"
            )
            self.total_money_label.configure(
                text=f"Total Today: {self.last_card.total_price:.2f}€", font=("Roboto", 30)
            )
        else:
            self.last_card = self.data_handler.get_current_card()
            self.check_card_date()
            self.create_widgets()
            self.load_widgets()

    def update_data(self, updated_card) -> None:
        self.last_card = updated_card
        self.card_hour, self.card_minutes = self.data_handler.get_current_card_total_hours(
            updated_card)

        self.price_h_label.configure(
            text=f"Price/h: {self.last_card.price_per_hour:.2f}€")
        self.total_time_label.configure(
            text=f"Time Today: {self.card_hour:02d}:{self.card_minutes:02d}h")
        self.pomo_num_label.configure(
            text=f"Pomodoros: {self.last_card.pomo_count}")
        self.total_money_label.configure(
            text=f"Total Today: {self.last_card.total_price:.2f}€")

    def update_info_buttons(self, count: int) -> None:
        if count == 0:
            [i.deselect() for i in self.radio_btn_list]
        else:
            self.radio_btn_list[count - 1].select()

    def show(self) -> None:
        self.pack(expand=True, fill="both", pady=7)
