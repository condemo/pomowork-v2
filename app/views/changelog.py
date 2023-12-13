import customtkinter as ctk
from config import _VERSION, APP_DIR
from config.theme import Colors


class ChangelogPopupWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master=master, fg_color=Colors.BACKGROUND)
        self.master = master
        x = self.master.winfo_width()
        y = self.master.winfo_height()
        self.geometry("500x600+%d+%d" % (x + 430, y + 190))
        self.title("New Version Changelog")

        self.read_changelog()
        self.create_widgets()
        self.load_widgets()

    def read_changelog(self) -> None:
        with open(APP_DIR / "CHANGELOG", "r") as file:
            self.text = file.read().split("----------------------------------------")

    def create_widgets(self) -> None:
        self.version_label = ctk.CTkLabel(
            self, text=f"What's new in version {_VERSION}?",
            font=("Roboto", 24), fg_color=Colors.PRIMARY)

        self.main_frame = ctk.CTkFrame(self, fg_color=Colors.BG_SECOND)
        # TODO: Cargar dinamicamente el texto
        self.text_label = ctk.CTkLabel(
            self.main_frame, text=self.text[0], font=("Roboto", 18), anchor="w")

        self.exit_frame = ctk.CTkFrame(
            self, fg_color=Colors.BG_SECOND)
        self.exit_btn = ctk.CTkButton(
            self.exit_frame, text="Close", fg_color=Colors.PRIMARY,
            font=("Roboto", 16), command=self.destroy)

    def load_widgets(self) -> None:
        self.version_label.pack(pady=5)

        self.main_frame.pack(expand=True, fill="both")
        self.text_label.pack()

        self.exit_frame.pack(pady=3)
        self.exit_btn.pack()
