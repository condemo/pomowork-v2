import customtkinter as ctk
from tkinter import StringVar, IntVar
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
        self.active_section = GeneralConfigFrame(self.section_frame, self.data_handler)
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
                self.active_section = GeneralConfigFrame(self.section_frame, self.data_handler)
                self.active_section.show()
                self.active_btn = self.general_btn
                self.active_btn.configure(fg_color="#2B2B2B")
            case 1:
                self.active_section = TimersConfigFrame(self.section_frame, self.data_handler)
                self.active_section.show()
                self.active_btn = self.timer_btn
                self.active_btn.configure(fg_color="#2B2B2B")
            case 2:
                self.active_section = AboutFrame(self.section_frame, self.data_handler)
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
    def __init__(self, master, data_handler: DataController):
        super().__init__(master=master)
        self.master = master
        self.data_handler = data_handler

        self.project_list = self.data_handler.get_project_list()
        print(self.project_list)

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.section = ctk.CTkFrame(self, border_width=2, border_color="red")
        self.center_frame = ctk.CTkFrame(self.section, fg_color="transparent")

        self.projects_container = ctk.CTkFrame(self.center_frame)
        self.last_open_project_label = ctk.CTkLabel(
            self.projects_container, text="Initial Project:")

    def load_widgets(self) -> None:
        self.section.pack(pady=10, padx=20, fill="x", ipady=10)
        self.center_frame.pack(expand=True)

        self.projects_container.pack()
        self.last_open_project_label.pack(side="left", pady=10)

    def show(self) -> None:
        self.pack(expand=True, fill="both")

    def remove(self) -> None:
        self.pack_forget()


class TimersConfigFrame(ctk.CTkFrame):
    def __init__(self, master, data_handler: DataController):
        super().__init__(master=master)
        self.master = master
        self.data_handler = data_handler

        work, short, long = self.data_handler.get_timers()

        self.work_value_label = StringVar(self, value=f"{work} mins")
        self.work_value_int = IntVar(self, value=f"{work}")

        self.short_value_label = StringVar(self, value=f"{short} mins")
        self.short_value_int = IntVar(self, value=f"{short}")

        self.long_value_label = StringVar(self, value=f"{long} mins")
        self.long_value_int = IntVar(self, value=f"{long}")

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.section = ctk.CTkFrame(self, border_width=2, border_color="red")
        self.center_frame = ctk.CTkFrame(self.section, fg_color="transparent")

        self.pomotimer_container = ctk.CTkFrame(self.center_frame)
        self.pomotimer_label = ctk.CTkLabel(
            self.pomotimer_container, text="Work Timer:", font=("Roboto", 20))
        self.pomotimer_slider = ctk.CTkSlider(
            self.pomotimer_container, from_=5, to=60, number_of_steps=11,
            variable=self.work_value_int, command=self.update_work)
        self.pomotimer_value = ctk.CTkLabel(
            self.pomotimer_container, textvariable=self.work_value_label, font=("Roboto", 20))

        self.short_timer_container = ctk.CTkFrame(self.center_frame)
        self.short_timer_label = ctk.CTkLabel(
            self.short_timer_container, text="Short Break:", font=("Roboto", 20))
        self.short_timer_slider = ctk.CTkSlider(
            self.short_timer_container, from_=1, to=20, number_of_steps=19,
            variable=self.short_value_int, command=self.update_short)
        self.short_timer_value = ctk.CTkLabel(
            self.short_timer_container, textvariable=self.short_value_label, font=("Roboto", 20))

        self.long_timer_container = ctk.CTkFrame(self.center_frame)
        self.long_timer_label = ctk.CTkLabel(
            self.long_timer_container, text="Long Break:", font=("Roboto", 20))
        self.long_timer_slider = ctk.CTkSlider(
            self.long_timer_container, from_=10, to=30, number_of_steps=4,
            variable=self.long_value_int, command=self.update_long)
        self.long_timer_value = ctk.CTkLabel(
            self.long_timer_container, textvariable=self.long_value_label, font=("Roboto", 20))

        self.save_btn = ctk.CTkButton(
            self.center_frame, text="Aplicar", command=self.save_timers)

    def load_widgets(self) -> None:
        self.section.pack(pady=10, padx=20, fill="x", ipady=10)
        self.center_frame.pack(expand=True)

        self.pomotimer_container.pack()
        self.pomotimer_label.pack(side="left", pady=10)
        self.pomotimer_slider.pack(side="left", padx=20)
        self.pomotimer_value.pack(side="left")

        self.short_timer_container.pack()
        self.short_timer_label.pack(side="left", pady=10)
        self.short_timer_slider.pack(side="left", padx=20)
        self.short_timer_value.pack(side="left")

        self.long_timer_container.pack()
        self.long_timer_label.pack(side="left", pady=10)
        self.long_timer_slider.pack(side="left", padx=20)
        self.long_timer_value.pack(side="left")

        self.save_btn.pack(pady=20)

    def update_work(self, val) -> None:
        self.work_value_label.set(f"{str(int(val))} mins")

    def update_short(self, val) -> None:
        self.short_value_label.set(f"{str(int(val))} mins")

    def update_long(self, val) -> None:
        self.long_value_label.set(f"{str(int(val))} mins")

    def save_timers(self) -> None:
        self.data_handler.save_timers_config(
            int(self.pomotimer_slider.get()),
            int(self.short_timer_slider.get()),
            int(self.long_timer_slider.get())
        )

    def show(self) -> None:
        self.pack(expand=True, fill="both")

    def remove(self) -> None:
        self.pack_forget()


class AboutFrame(ctk.CTkFrame):
    def __init__(self, master, data_handler: DataController):
        super().__init__(master=master)
        self.master = master
        self.data_handler = DataController

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
