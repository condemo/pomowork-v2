from typing import Optional
from lib.models import Card, Project
from lib.views import View
from data.cache import CacheHandler
import config


class ProjectDataHandler:
    def __init__(self, view: View):
        self.view = view
        self.cache_handler = CacheHandler()
        self.project_list = self.cache_handler.get_project_list()
        self.current_project: Project = self.cache_handler \
            .get_current_project()
        self.card_list = self.cache_handler.get_current_card_list()
        self.pomo_day_count = config.user_conf["pomo"]["pomo_day_count"]

    def get_project_list(self) -> list[tuple[int, str]]:
        return self.project_list

    def get_current_project_name(self) -> str:
        if self.current_project:
            return self.current_project.name

    def get_project_cards(self) -> list[Card]:
        return self.card_list

    def get_pomo_day_count(self) -> int:
        return self.pomo_day_count

    def save_pomo_day_count(self, count: int) -> int:
        self.pomo_day_count += count
        config.user_conf["pomo"]["pomo_day_count"] = self.pomo_day_count
        config.save_config(config.user_conf)
        return self.pomo_day_count

    @staticmethod
    def get_timers() -> tuple[int, int, int]:
        return (
            config.user_conf["pomo"]["pomo_timer"],
            config.user_conf["pomo"]["short_break"],
            config.user_conf["pomo"]["long_break"],
        )

    def switch_projects_state(self, state: bool) -> None:
        self.view.switch_projects_state(state)

    def change_current_project(self, id: int) -> Project:
        self.current_project = self.cache_handler.load_project_by_id(id)
        if self.current_project:
            self.card_list = self.cache_handler.get_current_card_list()
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

    def get_project_total_hours(self) -> tuple[int, int]:
        total_pomos: int = 0
        for card in self.card_list:
            total_pomos += card.pomo_count
        total_minutes = total_pomos * 30
        hours, minutes = divmod(total_minutes, 60)
        return hours, minutes

    def update_card_status(self, id: int, status: bool) -> Card:
        for card in self.card_list:
            if card.id == id:
                card.collected = status
                return self.cache_handler.update_card(card)

    def update_card(self, count: int = 0) -> None:
        self.current_card.pomo_count += count
        self.current_card.total_price = \
            (self.current_card.pomo_count / 2) * self.current_card.price_per_hour
        self.current_card = self.cache_handler.update_card(self.current_card)
        self.update_current_project_data()
        self.view.update_current_card(self.current_card)

    def update_card_price_h(self, card: Card, price: float) -> None:
        card.price_per_hour = price
        card.total_price = \
            (card.pomo_count / 2) * card.price_per_hour
        if card.id == self.current_card.id:
            self.current_card = self.cache_handler.update_card(card)
            self.view.update_current_card(self.current_card)
        else:
            self.cache_handler.update_card(card)

    def create_project(self, project_data: dict) -> Project:
        self.current_project = self.cache_handler.set_project(project_data)
        self.current_project_id = self.current_project.id

        return self.current_project

    def update_project(self, id: int, name: str, price: float) -> tuple[int, str, float]:
        updated_p = self.cache_handler.update_project(id, name, price)
        card = self.cache_handler.get_last_card_by_id(id)
        self.update_card_price_h(card, price)
        project = self.cache_handler.load_project_by_id(id)
        self.update_current_project_data(project)
        if self.current_project.id == id:
            self.current_project.name = name
            self.card_list = self.cache_handler.get_card_list_by_id(id)
            self.view.update_main_title()
        return updated_p

    def update_current_project_data(self, project: Optional[Project] = None) -> None:
        total: float = 0
        collected: float = 0
        pending: float = 0
        if project:
            card_list = self.cache_handler.get_card_list_by_id(project.id)
            for c in card_list:
                total += c.total_price
                if c.collected:
                    collected += c.total_price
                else:
                    pending += c.total_price
            project.total_money = total
            project.salary_collected = collected
            project.pending_salary = pending
            updated_p = self.cache_handler.update_project_data(project)
            if updated_p.id == self.current_project.id:
                self.current_project = updated_p
                self.card_list = self.cache_handler.get_card_list_by_id(self.current_project.id)
                self.view.update_project_data()
        else:
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
            self.card_list = self.cache_handler.get_card_list_by_id(self.current_project.id)
            self.view.update_project_data()

    def remove_project_by_id(self, id: int) -> None:
        if self.cache_handler.remove_project_by_id(id):
            return True
