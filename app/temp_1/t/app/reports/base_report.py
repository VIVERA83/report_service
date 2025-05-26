from collections import defaultdict
from typing import Generator, List, Type

from app.models.records import BaseRecord


class BaseReport:
    """Базовый класс для генерации отчетов.

    Attributes:
        _records: Список загруженных записей
        _max_lens: Максимальные длины значений для колонок
        indent: Размер отступа для форматирования
        subtotal_columns: Колонки для подсчета промежуточных итогов
        group: Поле для группировки данных
    """

    def __init__(self, data_class: Type["BaseRecord"], indent: int = 3) -> None:
        self._records: List["BaseRecord"] = []
        self._max_lens: dict[str, int] = defaultdict(int)
        self.indent = indent
        self.subtotal_columns = []
        self.group = ""
        self.data_class = data_class

    def _parse_file(self, file_name: str) -> Generator["BaseRecord", None, None]:
        """Парсит CSV-файл и возвращает записи."""
        with open(file_name, "r", encoding="utf-8") as f:
            keys = f.readline().strip().split(",")
            for line in f:
                values = line.strip().split(",")
                yield self.data_class(**dict(zip(keys, values)))

    def load_records(self, *files: str) -> None:
        """Загружает записи из файлов."""
        for file in files:
            self._records.extend(self._parse_file(file))
            self._update_column_widths()

    def sort_records(self, *fields: str) -> None:
        """Сортирует записи по указанным полям."""
        self._records.sort(key=lambda rec: [getattr(rec, field) for field in fields])

    def _update_column_widths(self) -> None:
        """Обновляет максимальные длины значений для колонок."""
        for record in self._records:
            for key, value in record.as_dict().items():
                self._max_lens[key] = max(self._max_lens[key], len(str(value)))