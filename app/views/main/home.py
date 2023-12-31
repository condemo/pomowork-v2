import customtkinter as ctk
from data.datahandlers import DataController
from views.main.frames import ProjectsFrame, CardsFrame, MainFrame
from views.changelog import ChangelogPopupWindow
from config.theme import Colors


class HomeView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, fg_color=Colors.BACKGROUND)
        self.pack_propagate(False)

        self.data_handler = DataController(self)
        self.winfo_toplevel().protocol("WM_DELETE_WINDOW", self.reset_pomo_day_count)
        self.create_widgets()
        self.load_widgets()

        self.created_window = None
        if self.data_handler.get_version_status():
            if self.created_window is None or not self.created_window.winfo_exists():
                self.created_window = ChangelogPopupWindow(self, self.data_handler)

    def create_widgets(self) -> None:
        self.projects_frame = ProjectsFrame(self, self.data_handler)
        self.main_frame = MainFrame(self, self.data_handler)
        self.cards_frame = CardsFrame(self, self.data_handler)

    def load_widgets(self) -> None:
        self.projects_frame.show()
        self.main_frame.show()
        self.cards_frame.show()

    def change_active_project(self, id: int) -> None:
        self.data_handler.change_current_project(id)
        self.main_frame.load_active_project()
        self.cards_frame.load_new_cards()
        self.cards_frame.update_project_data()

    def update_project_data(self) -> None:
        self.cards_frame.update_project_data()

    def update_current_card(self, current_card) -> None:
        self.main_frame.update_data(current_card)
        self.cards_frame.update_card_data(current_card)

    def update_main_title(self) -> None:
        self.main_frame.update_title()

    def switch_projects_state(self, state: bool) -> None:
        self.projects_frame.switch_projects_state(state)

    def update_info_buttons(self, count: int) -> None:
        self.main_frame.update_info_buttons(count)

    def reset_pomo_day_count(self) -> None:
        self.data_handler.save_pomo_day_count(0)
        self.winfo_toplevel().destroy()

    def reload_timers(self, timers: tuple[int]) -> None:
        self.main_frame.reload_timers(timers)

    def show(self) -> None:
        self.pack(expand=True, fill="both")

    def remove(self) -> None:
        self.pack_forget()
