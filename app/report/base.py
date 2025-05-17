from collections import defaultdict
from typing import Generator, Type

from app.core.dc import BaseRecord


class BaseReport:
    def __init__(self, dc: Type["BaseRecord"], indent: int = 3) -> None:
        self._records: list[BaseRecord] = []
        self._max_lens: dict[str, int] = defaultdict(int)
        self.indent = indent
        self.subtotal_columns = []
        self.group = ""
        self.dc = dc

    def __file_parse(self, file_name: str) -> Generator[BaseRecord, None, None]:
        with open(file_name, "r", encoding="utf-8") as f:
            keys = f.readline().strip().split(",")
            for line in f:
                string = line.strip().split(",")
                yield self.dc(**{key: value for key, value in zip(keys, string)})

    def load_records(self, *files: str):
        for file in files:
            for record in self.__file_parse(file):
                self._records.append(record)
                self._update_column_widths(record.as_dict())

    def sort_records(self, *fields: str):
        self._records.sort(key=lambda rec: [getattr(rec, field) for field in fields])

    def _update_column_widths(self, record: dict[str, str]):
        for key, value in record.items():
            if self._max_lens[key] < len(str(value)):
                self._max_lens[key] = len(str(value))

    def get_report(
        self,
        columns: dict[str, str] = None,
        subtotal_columns: list[str] = None,
        group: str = None,
    ) -> dict:
        raise NotImplementedError("Метод не определен")
