import time
from datetime import datetime
import threading
import customtkinter as ctk
import tkinter as tk
from CTkToolTip import CTkToolTip
from tkfontawesome import icon_to_image
from plyer import notification
from data.datahandlers import DataController
from utils.infomessage import InfoMessage
from views.main.configframe import ConfigWindow
from config import ASSETS_DIR
from config.theme import Colors
from playsound import playsound


BELL_FILE = ASSETS_DIR / "bell.ogg"


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


class ClockFrame(ctk.CTkFrame):
    def __init__(self, master, data_handler: DataController):
        super().__init__(
            master=master, fg_color=Colors.BG_SECOND, corner_radius=20,
            border_width=2, border_color=Colors.PRIMARY)
        self.master = master
        self.data_handler = data_handler

        self.time = tk.StringVar(self)

        self.stopped: bool = True
        self.paused: bool = True

        self.count = self.data_handler.get_pomo_day_count()
        self.pomo_timer, self.short_timer, self.long_timer = self.data_handler.get_timers()

        self.modes_list = ["Work", "Short Break", "Long Break"]
        self.current_mode_index = 0
        self.mode = self.modes_list[self.current_mode_index]
        self.set_timer(self.pomo_timer * 60)

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        # ICONS
        self.play_icon = icon_to_image("play", fill="white", scale=0.1)
        self.pause_icon = icon_to_image("pause", fill="white", scale=0.1)
        stop_icon = icon_to_image("stop", fill="white", scale=0.1)
        # WIDGETS
        self.mode_label = ctk.CTkLabel(self, text=f"{self.mode}", font=("Roboto", 40))

        self.main_frame = ctk.CTkFrame(self, fg_color=Colors.PRIMARY)
        self.timer_label = ctk.CTkLabel(
            self.main_frame, textvariable=self.time, font=("Roboto", 100))

        self.control_frame = ctk.CTkFrame(
            self.main_frame, fg_color=Colors.PRIMARY)
        self.pause_btn = ctk.CTkButton(
            self.control_frame, image=self.play_icon, text=" ", border_spacing=6, corner_radius=10,
            compound="right",
            fg_color=Colors.SECONDARY, hover_color=Colors.SECONDARY_HOVER, command=self.play)
        self.stop_btn = ctk.CTkButton(
            self.control_frame, text="", image=stop_icon, border_spacing=6, corner_radius=10,
            fg_color=Colors.ERROR, hover_color=Colors.ERROR_HOVER, command=self.stop)

    def load_widgets(self) -> None:
        self.mode_label.pack(pady=(5, 0))

        self.timer_label.pack()
        self.main_frame.place(relx=.5, rely=.5, anchor="center")

        self.pause_btn.pack(side="left", padx=10)
        self.stop_btn.pack(side="left", padx=10)
        self.control_frame.pack(fill="x", pady=10)

        CTkToolTip(self.pause_btn, message="Play/Pause", bg_color=Colors.BG_SECOND)
        CTkToolTip(self.stop_btn, message="Stop", bg_color=Colors.BG_SECOND)

    def back_mode(self) -> None:
        if self.stopped or self.paused:
            if self.current_mode_index == 0:
                self.current_mode_index = 2
                self.mode = self.modes_list[self.current_mode_index]
            else:
                self.current_mode_index -= 1
                self.mode = self.modes_list[self.current_mode_index]

            self.change_timer_mode()

            self.mode_label.configure(
                text=f"{self.mode}"
            )

    def forward_mode(self) -> None:
        if self.stopped or self.paused:
            if self.current_mode_index == 2:
                self.current_mode_index = 0
                self.mode = self.modes_list[self.current_mode_index]
            else:
                self.current_mode_index += 1
                self.mode = self.modes_list[self.current_mode_index]

            self.change_timer_mode()

            self.mode_label.configure(
                text=f"{self.mode}"
            )

    def change_timer_mode(self) -> None:
        match self.current_mode_index:
            case 0:
                new_timer = 60 * self.pomo_timer
            case 1:
                new_timer = 60 * self.short_timer
            case 2:
                new_timer = 60 * self.long_timer

        self.set_timer(new_timer)

    def set_timer(self, timer: float) -> None:
        self.timer = timer
        self.minutes, self.seconds = divmod(self.timer, 60)

        self.time.set(f"{int(self.minutes):02d}:{int(self.seconds):02d}")
        self.winfo_toplevel().update()

    def start_timer_thread(self) -> None:
        t = threading.Thread(target=self.start_timer)
        t.start()

    def start_timer(self) -> None:
        self.stopped = False
        self.paused = False

        while self.timer >= 0 and not self.paused and not self.stopped:
            self.set_timer(self.timer)
            time.sleep(.100)
            self.timer -= .100

        if not self.stopped and not self.paused:
            self.data_handler.switch_projects_state(True)
            match self.mode:
                case "Work":
                    self.data_handler.update_card(1)
                    self.data_handler.update_current_project_data()
                    self.pause_btn.configure(text=" ", image=self.play_icon)
                    self.data_handler.switch_ui_status(True)
                    self.stopped = True
                    self.count += 1
                    if self.count == 9:
                        self.count = 0
                        self.data_handler.save_pomo_day_count(self.count)
                        self.count = 1
                    self.data_handler.save_pomo_day_count(self.count)
                    if self.count == 4 or self.count == 8:
                        self.back_mode()
                    else:
                        self.forward_mode()
                    InfoMessage(self.winfo_toplevel(), "success", "Pomodoro acabado")
                    if not self.winfo_toplevel().focus_displayof():
                        notification.notify(
                            title="Timer Ended",
                            message="Ha acababo el pomodoro",
                            app_icon="",
                            timeout=5
                        )
                    playsound(BELL_FILE)
                case "Short Break":
                    self.stopped = True
                    self.pause_btn.configure(text=" ", image=self.play_icon)
                    self.data_handler.switch_ui_status(True)
                    self.back_mode()
                    InfoMessage(self.winfo_toplevel(), "info", "Descanso acabado")
                    if not self.winfo_toplevel().focus_displayof():
                        notification.notify(
                            title="Timer Ended",
                            message="Ha acababo el descanso corto",
                            app_icon="",
                            timeout=5
                        )
                    playsound(BELL_FILE)
                case "Long Break":
                    self.stopped = True
                    self.pause_btn.configure(text=" ", image=self.play_icon)
                    self.data_handler.switch_ui_status(True)
                    if self.count == 8:
                        self.count = 0
                        self.data_handler.save_pomo_day_count(self.count)

                    self.forward_mode()
                    InfoMessage(self.winfo_toplevel(), "info", "Descanso acabado")
                    if not self.winfo_toplevel().focus_displayof():
                        notification.notify(
                            title="Timer Ended",
                            message="Ha acababo el descanso largo",
                            app_icon="",
                            timeout=5
                        )
                    playsound(BELL_FILE)

    def stop(self) -> None:
        if self.stop_btn.cget("state") == "normal":
            self.stopped = True
            self.pause_btn.configure(text=" ", image=self.play_icon)
            self.change_timer_mode()
            self.data_handler.switch_projects_state(True)
            self.data_handler.switch_ui_status(True)
            self.stop_btn.configure(state="disable")

    def play(self) -> None:
        self.stop_btn.configure(state="normal")
        if self.pause_btn.cget("text") == "":
            self.pause_btn.configure(text=" ", image=self.play_icon)
            self.paused = True
            self.data_handler.switch_projects_state(True)
            self.data_handler.switch_ui_status(True)
        else:
            self.pause_btn.configure(text="", image=self.pause_icon)
            self.paused = False
            self.data_handler.switch_projects_state(False)
            self.start_timer_thread()
            self.data_handler.switch_ui_status(False)

    def reload_timers(self, timers: tuple[int]) -> None:
        self.pomo_timer, self.short_timer, self.long_timer = timers
        self.change_timer_mode()

    def show(self) -> None:
        self.pack(side="left", fill="both", expand=True)


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
