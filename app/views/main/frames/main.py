from datetime import datetime
import time
import threading
import customtkinter as ctk
import tkinter as tk
from lib.models import Card


class MainFrame(ctk.CTkFrame):
    def __init__(self, master, last_card: Card):
        super().__init__(master=master)
        self.master = master
        self.pack_propagate(False)
        self.last_card = last_card

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.pomo_frame = PomoFrame(self)
        self.info_frame = InfoFrame(self, self.last_card)

    def load_widgets(self) -> None:
        self.pomo_frame.show()
        self.info_frame.show()

    def load_new_data(self, last_card: Card) -> None:
        self.info_frame.pack_forget()
        self.last_card = last_card
        self.info_frame = InfoFrame(self, self.last_card)
        self.info_frame.show()

    def show(self) -> None:
        self.pack(side="left", expand=True, fill="both", padx=15)


class PomoFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.master = master
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

    def update_pomo_count(amount: int) -> None:
        print(f"Pomo sum: {amount}")

    def show(self) -> None:
        self.pack(expand=True, fill="both", pady=7)


class ClockFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.master = master
        print(
            self.master.master.master.last_card.pomo_count
        )

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

    def set_timer(self, timer: int = 60 * 1) -> None:
        self.timer = timer
        self.minutes, self.seconds = divmod(self.timer, 60)

        self.time.set(f"{self.minutes:02d}:{self.seconds:02d}")
        self.winfo_toplevel().update()

    def start_timer_thread(self) -> None:
        t = threading.Thread(target=self.start_timer)
        t.start()

    def start_timer(self) -> None:
        self.stopped = False
        self.paused = False

        while self.timer >= 0 and not self.paused and not self.stopped:
            # TODO: Al dormir 1 segundo en sistema es menos responsivo, buscar la manera de
            # hacerlo con floats
            self.set_timer(self.timer)
            time.sleep(1)
            self.timer -= 1

        # TODO: Implementar sistema para sumar un pomodoro a la tarjeta actual
        if not self.stopped and not self.paused:
            self.master.master.master.last_card.pomo_count += 1

    def stop(self) -> None:
        if self.stop_btn.cget("state") == "normal":
            self.stopped = True
            self.play_text.set("PL")
            self.set_timer()
            self.stop_btn.configure(state="disable")

    def play(self) -> None:
        self.stop_btn.configure(state="normal")
        # FIX: AL pulsar muy rápido el botón se general varios threads
        # y el tiempo baja muy rapido
        if self.play_text.get() == "II":
            self.play_text.set("PL")
            self.paused = True
        else:
            self.play_text.set("II")
            self.start_timer_thread()

    def show(self) -> None:
        self.pack(side="left", fill="both", expand=True)


class InfoFrame(ctk.CTkFrame):
    def __init__(self, master, last_card: Card):
        super().__init__(master=master)
        self.pack_propagate(False)
        self.last_card = last_card

        self.last_card_date = datetime.strptime(
            self.last_card.created_at, "%Y-%m-%d"
        ).strftime("%d/%m/%Y")

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.price_h_label = ctk.CTkLabel(
            self, text=f"Price/h: {self.last_card.price_per_hour}€", font=("Roboto", 18))
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

    def show(self) -> None:
        self.pack(expand=True, fill="both", pady=7)
