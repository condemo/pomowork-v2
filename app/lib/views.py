from typing import Protocol


class View(Protocol):
    def create_widget(self) -> None:
        ...

    def load_widget(self) -> None:
        ...

    def show(self) -> None:
        ...

    def remove(self) -> None:
        ...
