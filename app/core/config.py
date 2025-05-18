from enum import Enum


class ReportEnum(str, Enum):
    """Список отчетов.

    Сюда добавляем новый тип отчета.
    """

    payout = "payout"
    other = "other"

    @classmethod
    def to_list(cls) -> list[str]:
        """Возвращает список отчетов."""

        return list(cls.__members__.keys())
