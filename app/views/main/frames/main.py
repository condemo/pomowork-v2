import time
from datetime import datetime
import threading
import customtkinter as ctk
import tkinter as tk
from plyer import notification
from data.datahandlers import ProjectDataHandler
from utils.infomessage import InfoMessage


class MainFrame(ctk.CTkFrame):
    def __init__(self, master, data_handler: ProjectDataHandler):
        super().__init__(master=master)
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

    def show(self) -> None:
        self.pack(side="left", expand=True, fill="both", padx=15)


class PomoFrame(ctk.CTkFrame):
    def __init__(self, master, data_handler: ProjectDataHandler):
        super().__init__(master=master)
        self.master = master
        self.pack_propagate(False)
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                             weight=1, uniform="a")
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7),
                          weight=1, uniform="a")

        self.data_handler = data_handler

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.title_label = ctk.CTkLabel(
            self.top_frame, text=f"{self.data_handler.get_current_project_name()}",
            font=("Roboto", 28)
        )
        self.config_btn = ctk.CTkButton(
            self.top_frame, text="C", width=30, height=30, corner_radius=30)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.back_btn = ctk.CTkButton(
            self.main_frame, text="<", width=30, height=30,
            corner_radius=30, font=("Roboto", 50), fg_color="transparent",
            command=self.back_mode
        )
        self.clock_frame = ClockFrame(self.main_frame, self.data_handler)
        self.forward_btn = ctk.CTkButton(
            self.main_frame, text=">", width=30, height=30,
            corner_radius=30, font=("Roboto", 50), fg_color="transparent",
            command=self.forward_mode
        )

    def load_widgets(self) -> None:
        self.title_label.pack()
        self.config_btn.pack(side="right")
        self.top_frame.pack(fill="x", pady=10, padx=5)

        self.back_btn.pack(side="left")
        self.clock_frame.show()
        self.forward_btn.pack(side="left")
        self.main_frame.pack(fill="both", expand=True, padx=2, pady=2)

    def back_mode(self) -> None:
        self.clock_frame.back_mode()

    def forward_mode(self) -> None:
        self.clock_frame.forward_mode()

    def update_title(self) -> None:
        self.title_label.configure(
            text=f"{self.data_handler.get_current_project_name()}"
        )

    def show(self) -> None:
        self.pack(expand=True, fill="both", pady=7)


class ClockFrame(ctk.CTkFrame):
    def __init__(self, master, data_handler: ProjectDataHandler):
        super().__init__(master=master)
        self.master = master
        self.data_handler = data_handler

        self.time = tk.StringVar(self)
        self.set_timer()

        self.play_text = tk.StringVar(self)
        self.play_text.set("PL")

        self.stopped: bool = True
        self.paused: bool = True

        self.count = self.data_handler.get_pomo_day_count()
        self.pomo_timer, self.short_timer, self.long_timer = self.data_handler.get_timers()

        self.modes_list = ["Work", "Short Break", "Long Break"]
        self.current_mode_index = 0
        self.mode = self.modes_list[self.current_mode_index]

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.mode_label = ctk.CTkLabel(self, text=f"{self.mode}", font=("Roboto", 40))

        self.main_frame = ctk.CTkFrame(self)
        self.timer_label = ctk.CTkLabel(
            self.main_frame, textvariable=self.time, font=("Roboto", 100))

        self.control_frame = ctk.CTkFrame(self.main_frame)
        self.pause_btn = ctk.CTkButton(
            self.control_frame, textvariable=self.play_text, font=("Roboto", 50),
            fg_color="transparent", command=self.play)
        self.stop_btn = ctk.CTkButton(
            self.control_frame, text="ST", font=("Roboto", 50),
            fg_color="transparent", command=self.stop)

    def load_widgets(self) -> None:
        self.mode_label.pack()

        self.timer_label.pack()
        self.main_frame.place(relx=.5, rely=.5, anchor="center")

        self.pause_btn.pack(side="left", padx=10)
        self.stop_btn.pack(side="left", padx=10)
        self.control_frame.pack(fill="x", pady=10)

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

    def set_timer(self, timer: float = 60 * .1) -> None:
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
                    self.play_text.set("PL")
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
                case "Short Break":
                    self.play_text.set("PL")
                    self.stopped = True
                    self.back_mode()
                    InfoMessage(self.winfo_toplevel(), "info", "Descanso acabado")
                    if not self.winfo_toplevel().focus_displayof():
                        notification.notify(
                            title="Timer Ended",
                            message="Ha acababo el descanso corto",
                            app_icon="",
                            timeout=5
                        )
                case "Long Break":
                    self.play_text.set("PL")
                    self.stopped = True
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

    def stop(self) -> None:
        if self.stop_btn.cget("state") == "normal":
            self.stopped = True
            self.play_text.set("PL")
            self.set_timer()
            self.data_handler.switch_projects_state(True)
            self.stop_btn.configure(state="disable")

    def play(self) -> None:
        self.stop_btn.configure(state="normal")
        if self.play_text.get() == "II":
            self.play_text.set("PL")
            self.paused = True
            self.data_handler.switch_projects_state(True)
        else:
            self.play_text.set("II")
            self.paused = False
            self.data_handler.switch_projects_state(False)
            self.start_timer_thread()

    def show(self) -> None:
        self.pack(side="left", fill="both", expand=True)


class InfoFrame(ctk.CTkFrame):
    def __init__(self, master, data_handler: ProjectDataHandler):
        super().__init__(master=master)
        self.pack_propagate(False)
        self.data_handler = data_handler
        self.last_card = self.data_handler.get_current_card()

        if self.last_card:
            self.check_card_date()
            self.pomo_day_count = self.data_handler.get_pomo_day_count()
            self.create_widgets()
            self.load_widgets()

    def check_card_date(self) -> str:
        if self.last_card:
            self.last_card_date = datetime.strptime(
                self.last_card.created_at, "%Y-%m-%d"
            ).strftime("%d/%m/%Y")

    def create_widgets(self) -> None:
        self.price_h_label = ctk.CTkLabel(
            self, text=f"Price/h: {self.last_card.price_per_hour:.2f}€", font=("Roboto", 18))
        self.date_label = ctk.CTkLabel(self, text=f"{self.last_card_date}", font=("Roboto", 30))

        self.pomo_day_main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.pomo_day_left_frame = ctk.CTkFrame(self.pomo_day_main_frame, fg_color="transparent")
        self.pomo_day_right_frame = ctk.CTkFrame(self.pomo_day_main_frame, fg_color="transparent")

        self.radio_btn_list = [ctk.CTkRadioButton(
            self.pomo_day_left_frame, text="", width=10,
            state="normal", border_width_checked=10) for i in range(4)]
        [self.radio_btn_list.append(ctk.CTkRadioButton(
            self.pomo_day_right_frame, text="", width=10, state="readonly")) for i in range(4)]

        self.main_frame = ctk.CTkFrame(self)
        self.info_container_frame = ctk.CTkFrame(self.main_frame)
        self.pomo_num_label = ctk.CTkLabel(
            self.info_container_frame,
            text=f"Pomodoros: {self.last_card.pomo_count}", font=("Roboto", 50))

        self.bottom_frame = ctk.CTkFrame(self)
        self.total_money_label = ctk.CTkLabel(
            self.bottom_frame,
            text=f"Total Hoy: {self.last_card.total_price:.2f}€", font=("Roboto", 60))

    def load_widgets(self) -> None:
        self.price_h_label.place(relx=.03, rely=.014, anchor="nw")
        self.date_label.pack()

        self.pomo_day_main_frame.pack(pady=50)
        self.pomo_day_left_frame.pack(side="left", padx=15)
        self.pomo_day_right_frame.pack(side="left", padx=15)
        [i.pack(side="left") for i in self.radio_btn_list]
        [self.radio_btn_list[i].select() for i in range(self.pomo_day_count)]

        self.pomo_num_label.pack(pady=5)
        self.info_container_frame.pack(expand=True)
        self.main_frame.pack(expand=True, fill="both")

        self.total_money_label.pack(fill="x")
        self.bottom_frame.pack(fill="x")

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
            self.total_money_label.configure(
                text=f"Total Hoy: {self.last_card.total_price:.2f}€", font=("Roboto", 60)
            )
        else:
            self.last_card = self.data_handler.get_current_card()
            self.check_card_date()
            self.create_widgets()
            self.load_widgets()

    def update_data(self, updated_card) -> None:
        self.last_card = updated_card
        self.price_h_label.configure(
            text=f"Price/h: {self.last_card.price_per_hour:.2f}€")
        self.pomo_num_label.configure(
            text=f"Pomodoros: {self.last_card.pomo_count}")
        self.total_money_label.configure(
            text=f"Total Hoy: {self.last_card.total_price:.2f}€")

    def update_info_buttons(self, count: int) -> None:
        if count == 0:
            [i.deselect() for i in self.radio_btn_list]
        else:
            self.radio_btn_list[count - 1].select()

    def show(self) -> None:
        self.pack(expand=True, fill="both", pady=7)
