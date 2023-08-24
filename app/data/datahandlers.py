from lib.models import Card, Project
from data.cache import CacheHandler
from config import user_conf


class ProjectDataHandler:
    def __init__(self):
        # TODO: Implementar config para leer el proyecto que debe cargarse primero
        self.current_project_id = user_conf["core"]["last_open_project"]
        # TODO: Implementar el conseguir el current project id dentro de el propio handler
        self.cache_handler = CacheHandler(self.current_project_id)
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
            return self.current_project

    def get_current_card(self) -> Card:
        if self.card_list:
            return self.card_list[0]

    def create_project(self, project_data: dict) -> Project:
        self.current_project = self.cache_handler.set_project(project_data)
        self.current_project_id = self.current_project.id

        return self.current_project
