import time
import threading
import customtkinter as ctk
import tkinter as tk
from CTkToolTip import CTkToolTip
from plyer import notification
from playsound import playsound
from tkfontawesome import icon_to_image
from utils.infomessage import InfoMessage
from data.datahandlers import DataController
from config.theme import Colors
from config import ASSETS_DIR

BELL_FILE = ASSETS_DIR / "bell.ogg"


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
