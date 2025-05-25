from models.base import BaseRecord
from models.utils import resolve_aliases

HOURLY_RATE = ["hourly_rate", "rate", "salary"]


@resolve_aliases(aliases={"hourly_rate": HOURLY_RATE})
class Record(BaseRecord):
    """
    Специализированный класс для работы с записями о выплатах.

    Особенности:
        - Автоматический расчет поля payout
        - Поддержка псевдонимов для полей (через декоратор resolve_aliases)
    """

    def post_init(self):
        """
        Вычисляет выплату (payout) как произведение часов работы на ставку.
        Вызывается автоматически после инициализации объекта.
        """
        self["payout"] = self.multiply("hours_worked", "hourly_rate")
