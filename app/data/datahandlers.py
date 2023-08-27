from lib.models import Card, Project
from lib.views import View
from data.cache import CacheHandler


class ProjectDataHandler:
    def __init__(self, view: View):
        self.view = view
        self.cache_handler = CacheHandler()
        self.project_list = self.cache_handler.get_project_list()
        self.current_project: Project = self.cache_handler \
            .get_current_project()
        self.card_list = self.cache_handler.get_card_list()

    def get_project_list(self) -> list[tuple[int, str]]:
        return self.project_list

    def get_project_cards(self) -> list[Card]:
        return self.card_list

    def change_current_project(self, id: int) -> Project:
        self.current_project = self.cache_handler.load_project(id)
        if self.current_project:
            self.card_list = self.cache_handler.get_card_list()
            self.current_project_id = id

    def get_current_card(self) -> Card:
        if self.card_list:
            self.current_card = self.card_list[0]
            return self.current_card

    def update_card(self, count: int = 1) -> None:
        self.current_card.pomo_count += count
        self.current_card.total_price = \
            (self.current_card.pomo_count / 2) * self.current_card.price_per_hour
        self.current_card = self.cache_handler.update_card(self.current_card)
        self.view.update_current_card()

    def create_project(self, project_data: dict) -> Project:
        self.current_project = self.cache_handler.set_project(project_data)
        self.current_project_id = self.current_project.id

        return self.current_project
