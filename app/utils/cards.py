from datetime import date
from lib.models import Card
from data.datasend import create_new_card


class CardDataHandler:
    def __init__(self, card_list: list[Card]):
        # Determina si la última tarjeta es de hoy o de otro día anterior
        if card_list:
            last_card = card_list[0]
            if last_card.created_at == str(date.today()):
                self.last_card = last_card
            else:
                # Devuelve la última tarjeta o crea una nueva
                self.last_card = create_new_card({
                    "project_id": last_card.project_id,
                    "price_per_hour": last_card.price_per_hour,
                    "total_price": 0,
                    "collected": False
                })
        else:
            self.last_card = None

    def get_last_card(self) -> Card | None:
        return self.last_card
        # Tiene un método para actualizar la tarjeta
        # Envía una post request en caso de creación o actualización de una tarjeta
        # Actualiza el cache también
        # Crea una nueva tarjeta en caso de actualizar un pomo justo después de las 12??
        # Tiene un método para cambiar la tarjeta activa?????
