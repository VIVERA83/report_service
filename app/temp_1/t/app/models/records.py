from dataclasses import asdict, dataclass, field
from typing import Optional

from app.decorators.aliases import resolve_aliases


@dataclass
class BaseRecord:
    """Базовый класс для хранения записей данных.

    Attributes:
        Все поля должны быть определены в дочерних классах.
    """

    def __init__(self, *_, **__) -> None: ...

    def as_dict(self, *fields: Optional[str]) -> dict:
        """Конвертирует объект в словарь.

        Args:
            *fields: Поля для включения в результат. Если не указаны, возвращаются все поля.

        Returns:
            Словарь с данными объекта.
        """
        if not fields:
            return asdict(self)
        return {key: value for key, value in asdict(self).items() if key in fields}


@resolve_aliases(aliases={"hourly_rate": ["hourly_rate", "rate", "salary"]})
@dataclass(order=True)
class Record(BaseRecord):
    """Класс для хранения информации о рабочем времени и оплате.

    Attributes:
        id: Уникальный идентификатор записи
        name: Имя сотрудника
        email: Электронная почта
        department: Отдел
        hours_worked: Отработанные часы
        hourly_rate: Ставка в час
        payout: Автоматически рассчитываемая выплата (не инициализируется)
    """

    id: str
    name: str
    email: str
    department: str
    hours_worked: int
    hourly_rate: int
    payout: int = field(init=False)

    def __post_init__(self):
        """Рассчитывает выплату после инициализации объекта."""
        self.hours_worked = int(self.hours_worked)
        self.hourly_rate = int(self.hourly_rate)
        self.payout = self.hours_worked * self.hourly_rate