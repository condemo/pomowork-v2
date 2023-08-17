from datetime import date
from lib.models import Card
from data.datasend import CardDataSender


class CardDataHandler:
    def __init__(self, view, card_list: list[Card]):
        # Determina si la última tarjeta es de hoy o de otro día anterior
        self.home_view = view
        self.card_list = card_list
        self.data_sender = CardDataSender()
        if self.card_list:
            last_card = self.card_list[0]
            if last_card.created_at == str(date.today()):
                self.last_card = last_card
            else:
                # Devuelve la última tarjeta o crea una nueva
                self.last_card = self.data_sender.create_new_card({
                    "project_id": last_card.project_id,
                    "price_per_hour": last_card.price_per_hour,
                    "total_price": 0,
                    "collected": False
                })
        else:
            # FIX: Implementar mejor, siempre debe haber una tarjeta
            self.last_card = None

    def get_last_card(self) -> Card | None:
        return self.last_card

    def card_list(self) -> list[Card]:
        return self.card_list

    # Tiene un método para cambiar el proyecto activa
    def change_card_list(self, new_card_list: list[Card]) -> None:
        self.card_list = new_card_list

    # Tiene un método para actualizar la tarjeta
    def update_card(self, count: int = 0) -> None:
        self.last_card.pomo_count += count
        new_card = self.data_sender.update_card(self.last_card)
        if new_card:
            self.last_card = new_card
            self.home_view.update_current_card()
        # Envía una post o put request en caso de creación o actualización de una tarjeta
        # Actualiza el cache también
        # Crea una nueva tarjeta en caso de actualizar un pomo justo después de las 12??
