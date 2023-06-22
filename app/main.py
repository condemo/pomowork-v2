import customtkinter as ctk


class PomoWork(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self.title("PomoWork")


if __name__ == "__main__":
    app = PomoWork()
    app.mainloop()
