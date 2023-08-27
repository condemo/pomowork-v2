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

    def update_data(self) -> None:
        self.info_frame.update_data()

    def load_last_card(self) -> None:
        self.info_frame.load_last_card()

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
        self.config_btn = ctk.CTkButton(
            self.top_frame, text="C", width=30, height=30, corner_radius=30)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.back_btn = ctk.CTkButton(
            self.main_frame, text="<",
            width=30, height=30, corner_radius=30,
            font=("Roboto", 50), fg_color="transparent")
        self.clock_frame = ClockFrame(self.main_frame, self.data_handler)
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
    def __init__(self, master, data_handler: ProjectDataHandler):
        super().__init__(master=master)
        self.master = master
        self.data_handler = data_handler

        self.time = tk.StringVar(self)
        self.set_timer()

        self.play_text = tk.StringVar(self)
        self.play_text.set("PL")

        self.stopped: bool = False
        self.paused: bool = False

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.mode_label = ctk.CTkLabel(self, text="Work", font=("Roboto", 45))

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
            self.data_handler.update_card(1)
            self.play_text.set("PL")
            self.set_timer()
            InfoMessage(self.winfo_toplevel(), "success", "Pomodoro acabado")
            if not self.winfo_toplevel().focus_displayof():
                notification.notify(
                    title="Timer Ended",
                    message="Ha acababo el pomodoro",
                    app_icon="",
                    timeout=5
                )

    def stop(self) -> None:
        if self.stop_btn.cget("state") == "normal":
            self.stopped = True
            self.play_text.set("PL")
            self.set_timer()
            self.stop_btn.configure(state="disable")

    def play(self) -> None:
        self.stop_btn.configure(state="normal")
        if self.play_text.get() == "II":
            self.play_text.set("PL")
            self.paused = True
        else:
            self.play_text.set("II")
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

        self.pomo_num_label.pack(pady=5)
        self.info_container_frame.pack(expand=True)
        self.main_frame.pack(expand=True, fill="both")

        self.total_money_label.pack(fill="x")
        self.bottom_frame.pack(fill="x")

    def load_last_card(self) -> None:
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

    def update_data(self) -> None:
        self.last_card = self.data_handler.get_current_card()
        self.pomo_num_label.configure(
            text=f"Pomodoros: {self.last_card.pomo_count}")
        self.total_money_label.configure(
            text=f"Total Hoy: {self.last_card.total_price:.2f}€")

    def show(self) -> None:
        self.pack(expand=True, fill="both", pady=7)
