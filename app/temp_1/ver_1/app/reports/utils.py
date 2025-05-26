from typing import Generator, Type

from icecream import ic

from app.reports.types import BaseRecordT


def file_parse(
    file_name: str, cls: Type[BaseRecordT]
) -> Generator[BaseRecordT, None, None]:
    """
    Парсит CSV-файл и возвращает генератор объектов указанного класса

    Args:
        file_name: Путь к CSV-файлу
        cls: Класс (наследник BaseRecord) для создания объектов

    Yields:
        Экземпляры класса cls с данными из файла
    """
    with open(file_name, "r", encoding="utf-8") as f:
        keys = f.readline().strip().split(",")
        for line in f:
            values = line.strip().split(",")
            record_data = {key: value for key, value in zip(keys, values)}
            yield cls(**record_data)
