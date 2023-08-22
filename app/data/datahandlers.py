from lib.models import Card, Project
from data.cache import CacheHandler


class ProjectDataHandler:
    def __init__(self):
        self.cache_handler = CacheHandler()
        self.project_list = self.cache_handler.get_project_list()
        # TODO: Implementar config para leer el proyecto que debe cargarse primero
        self.current_project_id = 10
        self.current_project: Project = self.cache_handler \
            .get_project_info(self.current_project_id)

    def get_project_list(self) -> list[tuple[int, str]]:
        return self.project_list

    def get_project_cards(self) -> list[Card]:
        self.card_list = self.cache_handler.get_card_list()
        return self.card_list

    def change_current_project(self, id: int) -> Project:
        self.current_project = self.cache_handler.get_project_info(id)
        if self.current_project:
            self.current_project_id = id
            return self.current_project
