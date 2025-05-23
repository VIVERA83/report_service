from collections import defaultdict
from typing import List, Type

from app.models.utils import custom_sort
from app.reports.types import BaseRecordT
from app.reports.utils import file_parse


class BaseReport:
    """Базовый класс для генерации отчетов.

    Attributes:
        _records: Список загруженных записей
        _max_lens: Максимальные длины значений для колонок
        indent: Размер отступа для форматирования
        _subtotal_columns: Колонки для подсчета промежуточных итогов
        group: Поле для группировки данных
    """

    def __init__(self, model: Type[BaseRecordT]) -> None:
        self.model = model
        self._records: List[BaseRecordT] = []

        self._max_lens: dict[str, int] = defaultdict(int)
        self.indent = 3
        self._subtotal_columns = []
        self.group = ""

    def load_from_files(self, *files: str) -> None:
        """Загружает записей из файлов."""
        for file in files:
            self._records.extend(file_parse(file, self.model))

    def sort_records(self, *fields: str, reverse=False) -> None:
        """Сортирует записи по указанным полям."""
        for record in self._records:
            record.sort(by="custom", key_func=custom_sort(*fields), reverse=reverse)
        self._records.sort(
            key=lambda rec: [rec[key] for key in rec.keys() if key in fields],
            reverse=reverse,
        )

    def get_model_fields(self) -> dict[str, str]:
        if self._records:
            return {field: field for field in self._records[0].keys()}
        else:
            return {}


class JsonReport(BaseReport):

    def create_json_report(self, *fields: str, group: str = None) -> dict:
        (
            self.sort_records(group, *fields)
            if group is not None
            else self.sort_records(*fields)
        )
        fields = fields or self.get_model_fields()  # if fields else self._records[0].fields()
        result = defaultdict(dict)
        for report in self._records:
            if data := {key: value for key, value in report.items() if key in fields}:
                if group:
                    arr = result.get(report[group], {"items": []})
                    arr["items"].append(data)
                    result[report[group]] = arr
                else:
                    arr = result.get("items", [])
                    arr.append(data)
                    result["items"] = arr
        return result


class ShowReport(BaseReport):

    def __init__(self, model: Type[BaseRecordT]) -> None:
        super().__init__(model)
        self._title: dict[str, str] = defaultdict(str)
        self._subtotal_columns = []
        self._current_group = ""
        self._subtotal: dict[str, dict[str, int]] = defaultdict(dict)
        self._is_new_group = True
        self._result: list[str] = []

    def set_title_report(self, **fields) -> None:
        if not self._title:
            self._title = self.get_model_fields()

        for key, value in fields.items():
            if key in self._title:
                self._title[key] = str(value)
                self._max_lens[key] = max(len(value), self._max_lens[key])
            else:
                print(f"Указанная колонка `{key}` не найдена.")

    def show_report(
            self, *fields: str, group: str = None, subtotal_columns: dict[str, str] = None
    ) -> None:
        self.__clear(*fields, group=group, subtotal_columns=subtotal_columns)

        for record in self._records:
            main_line = self.__get_update_main_line(record, *fields)
            group_line = self.__get_update_group_line(record)
            sub_line = self.__get_update_sub_line(*fields)
            self.__update_subtotal(record)

            if sub_line:
                self._result.append(sub_line)
            if group_line:
                self._result.append(group_line)
            self._result.append(main_line)
        self._is_new_group = True
        sub_line = self.__get_update_sub_line(*fields)
        self._result.append(sub_line)

        return print(*self._result, sep="\n")

    def __get_title(self, *fields: str) -> str:
        if not len(self._title):
            self._title = self.get_model_fields()

        title = ""
        for field in fields or self._title.keys():
            title += " " * self.indent
            title += self._title[field].ljust(self._max_lens[field])
        return title

    def __update_column_widths(self) -> None:
        """Обновляет максимальные длины значений для колонок."""
        for field in self.get_model_fields():
            self._max_lens[field] = max(self._max_lens[field], len(str(field)))

        for record in self._records:
            for key, value in record.items():
                self._max_lens[key] = max(self._max_lens[key], len(str(value)))

    def __get_update_main_line(self, record: BaseRecordT, *fields: str) -> str:
        line = " " * self.indent
        for field in fields or self._title.keys():
            if self._title[field] == " ":
                line += "_" * self._max_lens[field]
            else:
                line += str(record[field]).ljust(self._max_lens[field])
            line += " " * self.indent
        return line

    def __get_update_group_line(self, record: BaseRecordT) -> str:
        if value := record.get(self.group):
            if self._current_group != value:
                self._current_group = value
                self._is_new_group = True
                return " " * self.indent + str(self._current_group)
        return ""

    def __get_update_sub_line(self, *fields: str) -> str:
        if self._is_new_group and len(self._subtotal) > 0:
            self._is_new_group = False
            line = " " * self.indent
            sub_total = [*self._subtotal.values()][-1]

            for key in fields or self._title.keys():
                if key in self._subtotal_columns:
                    line += str(sub_total[key]).ljust(self._max_lens[key])
                else:
                    line += " " * self._max_lens[key]
                line += " " * self.indent
            return line
        self._is_new_group = False
        return ""

    def __update_subtotal(self, record: BaseRecordT):
        for key, value in record.items():
            if key in self._subtotal_columns:
                if not self._subtotal.get(self._current_group):
                    self._subtotal[self._current_group] = defaultdict(int)
                self._subtotal[self._current_group][key] += record.sum(key)

    def __clear(self, *fields, group: str = None, subtotal_columns: list[str] = None):
        self.__update_column_widths()
        self.group = group or ""
        self._current_group = ""
        self._is_new_group = True
        self._subtotal = defaultdict(dict)
        self._subtotal_columns = subtotal_columns or []
        self._result = [self.__get_title(*fields)]
