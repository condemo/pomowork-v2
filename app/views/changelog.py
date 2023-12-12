import customtkinter as ctk


class ChangelogPopupWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master=master)
        self.master = master
        x = self.master.winfo_width()
        y = self.master.winfo_height()
        self.geometry("500x600+%d+%d" % (x + 430, y + 190))
        self.title("New Version Changelog")
