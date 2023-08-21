from lib.models import Card
from data.cache import CacheHandler


class ProjectDataHandler:
    def __init__(self):
        self.cache_handler = CacheHandler()
        self.project_list = self.cache_handler.get_project_list()
        # TODO: Implementar config para leer el proyecto que debe cargarse primero
        self.current_project_id = 10

    def get_project_list(self) -> list[tuple[int, str]]:
        return self.project_list

    def get_project_cards(self) -> list[Card]:
        card_list = self.cache_handler.get_card_list(self.current_project_id)
        card_list.sort(key=lambda e: e["id"])
        card_list.reverse()
        self.card_list = [Card(**card) for card in card_list]
        return self.card_list

    def create_card(self) -> Card:
        pass

    def change_current_project(self, id: int) -> None:
        self.current_project_id = id
