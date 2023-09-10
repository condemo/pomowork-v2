from typing import Optional
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

    def get_current_project_name(self) -> str:
        if self.current_project:
            return self.current_project.name

    def get_project_cards(self) -> list[Card]:
        return self.card_list

    def switch_projects_state(self, state: bool) -> None:
        self.view.switch_projects_state(state)

    def change_current_project(self, id: int) -> Project:
        self.current_project = self.cache_handler.load_project(id)
        if self.current_project:
            self.card_list = self.cache_handler.get_card_list()
            self.current_project_id = id

    def get_current_card(self) -> Card:
        if self.card_list:
            self.current_card = self.card_list[0]
            return self.current_card

    def get_project_total_info(self) -> tuple[float, float, float]:
        if self.current_project:
            return (
                self.current_project.pending_salary,
                self.current_project.salary_collected,
                self.current_project.total_money
            )

    def update_card_status(self, id: int, status: bool) -> Card:
        for card in self.card_list:
            if card.id == id:
                card.collected = status
                return self.cache_handler.update_card(card)

    def update_card(self, count: int = 0, new_price_h: Optional[float] = None) -> None:
        if new_price_h:
            self.current_card.price_per_hour = float(new_price_h)
        self.current_card.pomo_count += count
        self.current_card.total_price = \
            (self.current_card.pomo_count / 2) * self.current_card.price_per_hour
        self.current_card = self.cache_handler.update_card(self.current_card)
        self.update_project_data()
        self.view.update_current_card(self.current_card)

    def create_project(self, project_data: dict) -> Project:
        self.current_project = self.cache_handler.set_project(project_data)
        self.current_project_id = self.current_project.id

        return self.current_project

    def update_project(self, id: int, name: str, price: float) -> tuple[int, str, float]:
        updated_p = self.cache_handler.update_project(id, name, price)
        if updated_p:
            self.update_card(new_price_h=price)
        return updated_p

    def update_project_data(self) -> None:
        total: float = 0
        collected: float = 0
        pending: float = 0
        for card in self.card_list:
            total += card.total_price
            if card.collected:
                collected += card.total_price
            else:
                pending += card.total_price

        self.current_project.total_money = total
        self.current_project.salary_collected = collected
        self.current_project.pending_salary = pending
        self.current_project = self.cache_handler.update_project_data(self.current_project)
        self.card_list = self.cache_handler.get_card_list()
        self.view.update_project_data()
