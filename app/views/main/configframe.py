import customtkinter as ctk
from tkinter import StringVar, IntVar
from tkinter.messagebox import askyesno
from PIL import Image
import webbrowser
from data.datahandlers import DataController
from data.oauth2 import remove_session
from config import ASSETS_DIR, _VERSION, LICENSE_RESUME


class ConfigWindow(ctk.CTkToplevel):
    def __init__(self, master, data_handler: DataController):
        super().__init__(master=master)
        self.master = master
        self.geometry("900x500+200+200")
        self.title("Configuración")
        self.resizable(False, False)

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
        self.projects_names = [i[1] for i in self.project_list]

        self.init_mode_selected = self.data_handler.get_init_mode()
        self.init_mode_var = ctk.IntVar(self, value=0)

        self.load_selected_project()
        self.create_widgets()
        self.load_widgets()
        self.check_selection()

    def create_widgets(self) -> None:
        self.project_section = ctk.CTkFrame(self, border_width=2, border_color="red")
        self.center_frame = ctk.CTkFrame(self.project_section, fg_color="transparent")

        self.projects_container = ctk.CTkFrame(self.center_frame)

        self.startup_mode_label = ctk.CTkLabel(
            self.projects_container, text="Select inital load mode:", font=("Roboto", 20))
        self.startup_radio_container = ctk.CTkFrame(
            self.projects_container, fg_color="transparent")
        self.select_last_mode = ctk.CTkRadioButton(
            self.startup_radio_container, text="Last created project",
            variable=self.init_mode_var, value=1, command=self.update_init)
        self.select_project_mode = ctk.CTkRadioButton(
            self.startup_radio_container, text="Selected project",
            variable=self.init_mode_var, value=2, command=self.update_init)

        self.last_open_project_label = ctk.CTkLabel(
            self.projects_container, text="Select a project:", font=("Roboto", 16))
        self.projects_box = ctk.CTkComboBox(
            self.projects_container, width=180, values=self.projects_names,
            justify="center", font=("Roboto", 14), command=self.update_start_project,
            state="readonly")

        self.appearance_section = ctk.CTkFrame(self, border_width=2, border_color="red")
        self.appearance_title = ctk.CTkLabel(
            self.appearance_section, text="Appearance", font=("Roboto", 24))
        self.coming_soon_label = ctk.CTkLabel(
            self.appearance_section, text="(Coming Soon)")

    def load_widgets(self) -> None:
        self.project_section.pack(pady=10, padx=20, fill="x", ipady=10)
        self.center_frame.pack(expand=True)

        self.projects_container.pack()

        self.startup_mode_label.pack()
        self.startup_radio_container.pack(pady=10)
        self.select_last_mode.pack(side="left", padx=10)
        self.select_project_mode.pack(side="left", padx=10)

        self.last_open_project_label.pack(side="left", pady=10)
        self.projects_box.pack(side="left", padx=20)

        self.appearance_section.pack(pady=10, padx=20, fill="x", ipady=10)
        self.appearance_title.pack(pady=10)
        self.coming_soon_label.pack()

    def load_selected_project(self) -> None:
        self.startup_project_id = self.data_handler.get_startup_project()
        for p in self.project_list:
            if p[0] == self.startup_project_id:
                self.startup_project_name = p[1]

    def update_start_project(self, choice) -> None:
        for project in self.project_list:
            if project[1] == choice:
                self.data_handler.save_new_last_open_project(project[0])

    def check_selection(self) -> None:
        match self.init_mode_selected:
            case "last":
                self.init_mode_var.set(1)
                self.projects_box.configure(state="disabled")
                self.last_open_project_label.configure(text_color="grey")
            case "selection":
                self.init_mode_var.set(2)
                self.projects_box.set(self.startup_project_name)

    def update_init(self) -> None:
        match self.init_mode_var.get():
            case 1:
                self.projects_box.configure(state="disabled")
                self.last_open_project_label.configure(text_color="grey")
                self.data_handler.update_config_settings("initial_mode", "last")
            case 2:
                self.projects_box.configure(state="normal")
                self.last_open_project_label.configure(text_color="white")
                self.data_handler.update_config_settings("initial_mode", "selection")

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
        super().__init__(master=master, fg_color="transparent")
        self.master = master
        self.data_handler = DataController

        self.load_background()
        self.create_widgets()
        self.load_widgets()

    def load_background(self) -> None:
        bg_img = ctk.CTkImage(Image.open(ASSETS_DIR / "about-background.jpeg"),
                              size=(900, 900))

        self.bg_img_label = ctk.CTkLabel(self, text="", image=bg_img)
        self.bg_img_label.place(x=0, y=0, anchor="nw", relwidth=1, relheight=1)

    def create_widgets(self) -> None:
        img = Image.open(ASSETS_DIR / "pomowork_icon.png")
        github_img = Image.open(ASSETS_DIR / "github-mark.png")

        self.tabview = ctk.CTkTabview(self, fg_color="white", bg_color="white",
            corner_radius=10, segmented_button_fg_color="black", text_color="white",
            segmented_button_selected_color="#A82325")
        self.about_tab = self.tabview.add("About")
        self.credits_tab = self.tabview.add("Credits")
        self.license_tab = self.tabview.add("License")

        # ABOUT TAB
        self.logo_img = ctk.CTkImage(dark_image=img, size=(150, 150))
        self.logo_label = ctk.CTkLabel(self.about_tab, image=self.logo_img, text="")
        self.app_name_label = ctk.CTkLabel(
            self.about_tab, text="Pomowork", font=("Roboto", 30, "bold"), text_color="black")
        self.version_label = ctk.CTkLabel(self.about_tab, text=_VERSION, font=("Roboto", 15),
            text_color="grey")
        self.description_label = ctk.CTkLabel(self.about_tab, font=("Roboto", 18, "bold"),
            text_color="grey", text="Manage your time and payments")
        self.github_img = ctk.CTkImage(dark_image=github_img, size=(30, 30))
        self.github_btn = ctk.CTkButton(
            self.about_tab, image=self.github_img, text="Github",
            font=("Roboto", 14), text_color="black", fg_color="transparent",
            compound="top", width=50, cursor="hand2", hover=False,
            command=lambda: webbrowser.open_new("https://github.com/condemo/pomowork-v2"))
        self.copyright_label = ctk.CTkLabel(
            self.about_tab, text="\u00A9 Copyright 2023", font=("Roboto", 12, "bold"))

        # CREDITS TAB
        self.credits_frame = ctk.CTkFrame(
            self.credits_tab, fg_color="transparent")
        self.credits_info_label = ctk.CTkLabel(
            self.credits_frame, text="Gustavo de los Santos\n<gustleo.dev@gmail.com>",
            text_color="black")

        # LICENSE TAB
        self.license_frame = ctk.CTkFrame(self.license_tab)
        self.license_label = ctk.CTkLabel(self.license_frame, text=LICENSE_RESUME)
        self.license_link_label = ctk.CTkLabel(
            self.license_tab, text="Full License", cursor="hand2", text_color="blue")
        self.license_link_label.bind("<Button-1>", lambda: webbrowser.open_new(
            "https://www.gnu.org/licenses/gpl-3.0.html"))

    def load_widgets(self) -> None:
        self.tabview.pack(pady=5)
        self.logo_label.pack()

        self.app_name_label.pack()
        self.version_label.pack()
        self.description_label.pack()
        self.github_btn.pack(pady=5)
        self.copyright_label.pack()

        self.credits_frame.pack(ipadx=10, ipady=10)
        self.credits_info_label.pack(expand=True)

        self.license_frame.pack()
        self.license_label.pack(padx=5)
        self.license_link_label.pack()

    def show(self) -> None:
        self.pack(expand=True, fill="both", ipadx=5, ipady=5)

    def remove(self) -> None:
        self.pack_forget()
