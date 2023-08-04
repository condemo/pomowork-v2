from datetime import datetime
import customtkinter as ctk
import tkinter as tk
from lib.models import Card


class MainFrame(ctk.CTkFrame):
    def __init__(self, master, last_card: Card):
        super().__init__(master=master)
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

        self.min = tk.StringVar(self)
        self.min.set("30")
        self.sec = tk.StringVar(self)
        self.sec.set("00")
        self.time = tk.StringVar(self)
        self.time.set(self.min.get() + ":" + self.sec.get())

        self.play_text = tk.StringVar(self)
        self.play_text.set("II")

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.mode_label = ctk.CTkLabel(self, text="Work", font=("Roboto", 45))

        self.main_frame = ctk.CTkFrame(self)
        self.timer = ctk.CTkLabel(
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

        self.timer.pack()
        self.main_frame.place(relx=.5, rely=.5, anchor="center")

        self.pause_btn.pack(side="left", padx=10)
        self.stop_btn.pack(side="left", padx=10)
        self.control_frame.pack(fill="x", pady=10)

    def stop(self) -> None:
        if self.stop_btn.cget("state") == "normal":
            print("STOP")
            self.stop_btn.configure(state="disable")

    def play(self) -> None:
        self.stop_btn.configure(state="normal")
        if self.play_text.get() == "II":
            self.play_text.set("PL")
        else:
            self.play_text.set("II")
        print("PLAY")

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
