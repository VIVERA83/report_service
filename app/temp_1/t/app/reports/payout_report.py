from typing import Dict, List, Optional

from .base_report import BaseReport


class PayoutReport(BaseReport):
    """Класс для генерации отчетов о выплатах."""

    def get_report(
            self,
            columns: Optional[Dict[str, str]] = None,
            subtotal_columns: Optional[List[str]] = None,
            group: Optional[str] = None
    ) -> dict:
        """Генерирует отчет в формате JSON."""
        # Полная реализация метода
        ...

    def _generate_visual_report(self, columns: Dict[str, str]) -> None:
        """Формирует визуальное представление отчета."""
        # Полная реализация метода
        ...