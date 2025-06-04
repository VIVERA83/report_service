from collections import defaultdict
from typing import Type, Generator

from data_reporter.record.base import BaseRecord
from data_reporter.report.utils import custom_sort


class BaseReport:
    """
    Базовый класс для генерации отчетов

    Attributes:
        model (Type[BaseRecord]): Класс модели данных
        _records (list[BaseRecord]): Загруженные записи
        _max_lens (dict[str, int]): Максимальные длины значений колонок
        indent (int): Размер отступа между колонками
        _subtotal_columns (list): Колонки для промежуточных итогов
        group (str): Поле для группировки данных

    Методы:
        load_from_files(): Загрузка данных из файлов
        sort_records(): Сортировка записей
        get_model_fields(): Получение полей модели
    """

    class Meta:
        model: Type[BaseRecord] = BaseRecord

    def __init__(self) -> None:
        self.model = self.Meta.model
        self._records: list[BaseRecord] = []

        self._max_lens: dict[str, int] = defaultdict(int)
        self.indent = 3
        self._subtotal_columns = []
        self.group = ""

    def load_from_files(self, *files: str) -> None:
        """
        Загружает данные из файлов

        Параметры:
            files (str): Список путей к файлам

        Пример:
            >>> report = BaseReport()
            >>> report.load_from_files("data.csv")
        """
        for file in files:
            self._records.extend(self._file_parse(file))

    def sort_records(self, *fields: str, reverse=False) -> None:
        """
        Сортирует записи по указанным полям

        Параметры:
            fields (str): Поля для сортировки
            reverse (bool): Обратный порядок сортировки
        """
        for record in self._records:
            record.sort(by="custom", key_func=custom_sort(*fields), reverse=reverse)
        self._records.sort(
            key=lambda rec: [rec[key] for key in rec.keys() if key in fields],
            reverse=reverse,
        )

    def get_model_fields(self) -> dict[str, str]:
        """
        Возвращает поля модели

        Возвращает:
            dict: Словарь {название_поля: название_колонки}
        """
        if self._records:
            return {field: field for field in self._records[0].keys()}
        else:
            return {}

    def _file_parse(
            self, file_name: str,
    ) -> Generator[BaseRecord, None, None]:
        """
        Парсит CSV-файл и возвращает генератор объектов указанного класса

        Args:
            file_name: Путь к CSV-файлу

        Yields:
            Экземпляры класса cls с данными из файла
        """
        with open(file_name, "r", encoding="utf-8") as f:
            keys = f.readline().strip().split(",")
            for line in f:
                values = line.strip().split(",")
                record_data = {key: value for key, value in zip(keys, values)}
                yield self.model(**record_data)
