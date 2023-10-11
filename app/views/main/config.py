import customtkinter as ctk
from tkinter.messagebox import askyesno
from data.datahandlers import ProjectDataHandler
from data.oauth2 import remove_session


class ConfigWindow(ctk.CTkToplevel):
    def __init__(self, master, data_handler: ProjectDataHandler):
        super().__init__(master=master)
        self.master = master
        self.geometry("1000x600+200+200")
        self.title("Configuración")

        self.data_handler = data_handler

        self.create_widgets()
        self.load_widgets()

    def create_widgets(self) -> None:
        self.menu_frame = ctk.CTkFrame(self, fg_color="blue")
        self.logout_btn = ctk.CTkButton(
            self.menu_frame, text="Logout", fg_color="red",
            font=("Roboto", 18, "bold"), corner_radius=10,
            command=self.logout)
        self.section_frame = ctk.CTkFrame(self, fg_color="yellow")

    def load_widgets(self) -> None:
        self.menu_frame.pack(side="left", fill="y")
        self.logout_btn.place(anchor="sw", relx=0, rely=1, relwidth=1, relheight=.06)
        self.section_frame.pack(expand=True, fill="both", side="left")

    def logout(self) -> None:
        logout_confirm = askyesno("Logout", "You are about to log out, are you sure?", parent=self)
        if logout_confirm:
            remove_session()
            self.master.winfo_toplevel().go_login_view()
            self.destroy()
