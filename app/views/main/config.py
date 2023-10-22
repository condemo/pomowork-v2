import customtkinter as ctk
from tkinter.messagebox import askyesno
from data.datahandlers import DataController
from data.oauth2 import remove_session


class ConfigWindow(ctk.CTkToplevel):
    def __init__(self, master, data_handler: DataController):
        super().__init__(master=master)
        self.master = master
        self.geometry("1000x600+200+200")
        self.title("Configuración")

        self.data_handler = data_handler

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.menu_frame = ctk.CTkFrame(self, border_width=1)
        self.general_btn = ctk.CTkButton(
            self.menu_frame, text="General", font=("Roboto", 20),
            width=250, height=100, fg_color="#2B2B2B",
            command=lambda: self.switch_section(0))
        self.timer_btn = ctk.CTkButton(
            self.menu_frame, text="Timers", font=("Roboto", 20),
            width=250, height=100, fg_color="grey",
            command=lambda: self.switch_section(1))
        self.about_btn = ctk.CTkButton(
            self.menu_frame, text="About", font=("Roboto", 20),
            width=250, height=100, fg_color="grey",
            command=lambda: self.switch_section(2))

        self.logout_btn = ctk.CTkButton(
            self.menu_frame, text="Logout", fg_color="red",
            font=("Roboto", 18, "bold"), corner_radius=10,
            command=self.logout)

        self.section_frame = ctk.CTkFrame(self)
        self.active_section = GeneralConfigFrame(self.section_frame)
        self.active_btn = self.general_btn

    def load_widgets(self) -> None:
        self.menu_frame.pack(side="left", fill="y")
        self.general_btn.pack(side="top", pady=2, padx=2)
        self.timer_btn.pack(side="top", pady=2, padx=2)
        self.about_btn.pack(side="top", pady=2, padx=2)
        self.logout_btn.place(anchor="sw", relx=0, rely=1, relwidth=1, relheight=.06)

        self.section_frame.pack(expand=True, fill="both", side="left")

        self.active_section.show()

    def switch_section(self, section_index: int) -> None:
        self.active_section.remove()
        self.active_btn.configure(fg_color="grey")
        match section_index:
            case 0:
                self.active_section = GeneralConfigFrame(self.section_frame)
                self.active_section.show()
                self.active_btn = self.general_btn
                self.active_btn.configure(fg_color="#2B2B2B")
            case 1:
                self.active_section = TimersConfigFrame(self.section_frame)
                self.active_section.show()
                self.active_btn = self.timer_btn
                self.active_btn.configure(fg_color="#2B2B2B")
            case 2:
                self.active_section = AboutFrame(self.section_frame)
                self.active_section.show()
                self.active_btn = self.about_btn
                self.active_btn.configure(fg_color="#2B2B2B")

    def logout(self) -> None:
        logout_confirm = askyesno("Logout", "You are about to log out, are you sure?", parent=self)
        if logout_confirm:
            remove_session()
            self.master.winfo_toplevel().go_login_view()
            self.destroy()


class GeneralConfigFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.master = master

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.title = ctk.CTkLabel(self, text="Coming Soon", font=("Roboto", 25))

    def load_widgets(self) -> None:
        self.title.pack()

    def show(self) -> None:
        self.pack(expand=True, fill="both")

    def remove(self) -> None:
        self.pack_forget()


class TimersConfigFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.master = master

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.title = ctk.CTkLabel(self, text="Coming Soon", font=("Roboto", 25))

    def load_widgets(self) -> None:
        self.title.pack()

    def show(self) -> None:
        self.pack(expand=True, fill="both")

    def remove(self) -> None:
        self.pack_forget()


class AboutFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.master = master

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.title = ctk.CTkLabel(self, text="Coming Soon", font=("Roboto", 25))

    def load_widgets(self) -> None:
        self.title.pack()

    def show(self) -> None:
        self.pack(expand=True, fill="both")

    def remove(self) -> None:
        self.pack_forget()
