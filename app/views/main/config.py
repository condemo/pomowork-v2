import customtkinter as ctk
from data.datahandlers import ProjectDataHandler


class ConfigWindow(ctk.CTkToplevel):
    def __init__(self, master, data_handler: ProjectDataHandler):
        super().__init__(master=master)
        self.master = master
        self.geometry("1000x600+200+200")
        self.title("Configuración")

        self.data_handler = data_handler
