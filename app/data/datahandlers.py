from typing import Optional
from lib.models import Card, Project
from lib.views import View
from data.cache import CacheHandler
import config


class DataController:
    def __init__(self, view: View):
        self.view = view
        self.cache_handler = CacheHandler(view)
        self.project_list = self.cache_handler.get_project_list()
        # if not config.user_conf["core"]["startup_project"] and self.project_list:
        #     self.save_new_last_open_project(self.project_list[0][0])
        #     self.cache_handler.update_last_open_project(self.project_list[0][0])
        if config.user_conf["config"]["initial_mode"] == "last":
            self.cache_handler.load_project_by_id(self.project_list[0][0])
        elif config.user_conf["config"]["initial_mode"] == "selection":
            self.cache_handler.load_project_by_id(config.user_conf["core"]["startup_project"])
        self.current_project: Project = self.cache_handler \
            .get_current_project()
        self.card_list = self.cache_handler.get_current_card_list()
        self.pomo_day_count = config.user_conf["pomo"]["pomo_day_count"]

    def get_project_list(self) -> list[tuple[int, str, float]]:
        return self.project_list

    def get_current_project_name(self) -> str:
        if self.current_project:
            return self.current_project.name

    def get_project_cards(self) -> list[Card]:
        return self.card_list

    def get_pomo_day_count(self) -> int:
        return self.pomo_day_count

    @staticmethod
    def get_startup_project() -> int:
        return config.user_conf["core"]["startup_project"]

    @staticmethod
    def get_init_mode() -> str:
        return config.user_conf["config"]["initial_mode"]

    @staticmethod
    def save_new_last_open_project(id: int | bool) -> None:
        config.user_conf["core"]["startup_project"] = id
        config.save_config(config.user_conf)

    @staticmethod
    def update_config_settings(key: str, val: str) -> None:
        if key == "initial_mode" and val == "last":
            config.user_conf["core"]["startup_project"] = False

        config.user_conf["config"][key] = val
        config.save_config(config.user_conf)

    def save_pomo_day_count(self, count: int) -> int:
        self.pomo_day_count = count
        config.user_conf["pomo"]["pomo_day_count"] = self.pomo_day_count
        config.save_config(config.user_conf)
        self.view.update_info_buttons(self.pomo_day_count)
        return self.pomo_day_count

    def save_timers_config(self, work: int, short: int, long: int) -> None:
        config.user_conf["pomo"]["pomo_timer"] = work
        config.user_conf["pomo"]["short_break"] = short
        config.user_conf["pomo"]["long_break"] = long
        config.save_config(config.user_conf)
        self.view.reload_timers((work, short, long))

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

    def get_current_card_total_hours(self, card: Optional[Card] = None) -> tuple[int, int]:
        if card:
            total_minutes = card.pomo_count * int(config.user_conf["pomo"]["pomo_timer"])
        else:
            total_minutes = self.current_card.pomo_count * \
                int(config.user_conf["pomo"]["pomo_timer"])
        hours, minutes = divmod(total_minutes, 60)
        print(total_minutes)
        return (hours, minutes)

    def get_project_total_info(self) -> tuple[float, float, float]:
        if self.current_project:
            return (
                self.current_project.pending_salary,
                self.current_project.salary_collected,
                self.current_project.total_money
            )
        else:
            return (0, 0, 0)

    def get_project_total_hours(self) -> tuple[int, int]:
        total_pomos: int = 0
        if self.card_list:
            for card in self.card_list:
                total_pomos += card.pomo_count
            total_minutes = total_pomos * int(config.user_conf["pomo"]["pomo_timer"])
            hours, minutes = divmod(total_minutes, 60)
            return hours, minutes
        else:
            return 0, 0

    def update_card_status(self, id: int, status: bool) -> Card:
        for card in self.card_list:
            if card.id == id:
                card.collected = status
                return self.cache_handler.update_card(card.__dict__)

    def update_card(self, count: int = 0) -> None:
        self.current_card.pomo_count += count
        self.current_card.total_price = \
            (self.current_card.pomo_count / 2) * self.current_card.price_per_hour
        self.current_card = self.cache_handler.update_card(self.current_card.__dict__)
        self.update_current_project_data()
        self.view.update_current_card(self.current_card)

    def update_card_price_h(self, card: Card, price: float) -> None:
        card.price_per_hour = price
        card.total_price = \
            (card.pomo_count / 2) * card.price_per_hour
        if card.id == self.current_card.id:
            self.current_card = self.cache_handler.update_card(card.__dict__)
            self.view.update_current_card(self.current_card)
        else:
            self.cache_handler.update_card(card.__dict__)

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
            for p in self.project_list:
                if p[0] == id:
                    self.project_list.remove(p)
            return True
