import customtkinter as ctk
import threading
from typing import Literal
from config.theme import Colors


class InfoMessage(ctk.CTkFrame):
    def __init__(self, master,
                 mode: Literal["error", "info", "success"], text: str):
        match mode:
            case "error":
                background_color = Colors.ERROR
            case "info":
                background_color = Colors.INFO
            case "success":
                background_color = Colors.BG_CARDS

        super().__init__(
            master=master, fg_color=background_color, corner_radius=5)

        self.text = text

        self.x_pos = 1
        self.relwidth = .25
        self.load_widgets()
        self.show()

    def load_widgets(self) -> None:
        self.text_label = ctk.CTkLabel(self, text=self.text, font=("Roboto", 22))
        self.text_label.pack(expand=True, padx=2, pady=2)

    def animate(self) -> None:
        self.x_pos -= .006
        if self.x_pos >= 1 - self.relwidth:
            self.place(relx=self.x_pos, rely=0.01, relwidth=self.relwidth, relheight=.09)
            self.winfo_toplevel().after(20, self.animate)
        elif self.x_pos >= .74:
            self.winfo_toplevel().after(1500, self.animate)
        else:
            self.remove()

    def start_animate(self) -> None:
        t = threading.Thread(target=self.animate)
        t.start()

    def remove(self) -> None:
        self.place_forget()

    def show(self) -> None:
        self.place(relx=self.x_pos, rely=0, relwidth=self.relwidth, relheight=.09)
        self.start_animate()
