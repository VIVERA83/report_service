from collections import defaultdict
from typing import Type

from icecream import ic

from app.models.base import BaseRecord
from app.models.utils import custom_sort
from app.reports.types import BaseRecordT
from app.reports.utils import file_parse


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
        model: Type[BaseRecord] #= BaseRecord

    def __init__(self) -> None:
        self.model = self.Meta.model
        ic(self.model)
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
            self._records.extend(file_parse(file, self.model))

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


class JsonReport(BaseReport):
    """
    Класс для генерации структурированных отчетов в JSON-формате

    Наследует:
        BaseReport

    Методы:
        create_json_report(): Формирует отчет с группировкой
    """

    def create_json_report(self, *fields: str, group: str = None) -> dict:
        """
        Создает отчет с возможностью группировки

        Параметры:
            fields (str): Поля для включения в отчет
            group (str): Поле для группировки

        Возвращает:
            dict: Отчет в формате:
                {
                    "group1": {"items": [records]},
                    ...
                }

            Пример:
                >>> report = JsonReport()
                >>> report.load_from_files("data.csv")
                >>> result = report.create_json_report("name", "hours", group="department")
        """
        (
            self.sort_records(group, *fields)
            if group is not None
            else self.sort_records(*fields)
        )
        fields = fields or self.get_model_fields()
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
    """
    Класс для форматированного вывода отчетов в консоль

    Наследует:
        BaseReport

    Методы:
        set_title_report(): Настройка заголовков
        show_report(): Вывод отчета
        set_symbol(): Установка символов форматирования
    """

    def __init__(self) -> None:
        super().__init__()
        self._title: dict[str, str] = defaultdict(str)
        self._subtotal_columns = []
        self._current_group = ""
        self._subtotal: dict[str, dict[str, int]] = defaultdict(dict)
        self._is_new_group = True
        self._result: list[str] = []
        self._symbol = defaultdict(str)

    def set_title_report(self, **fields) -> None:
        """
        Задает пользовательские заголовки колонок

        Параметры:
            **fields (str): Пары {поле: новый_заголовок}

        Пример:
            >>> report.set_title_report(name="Сотрудник", hours="Часы")
        """
        if not self._title:
            self._title = self.get_model_fields()

        for key, value in fields.items():
            if key in self._title:
                self._title[key] = str(value)
                self._max_lens[key] = max(len(str(value)), self._max_lens[key])
            else:
                print(f"Указанная колонка `{key}` не найдена.")

    def show_report(
        self, *fields: str, group: str = None, subtotal_columns: list[str] = None
    ) -> None:
        """
        Выводит форматированный отчет в консоль

        Параметры:
        fields (str): Поля для отображения
        group (str): Поле группировки
        subtotal_columns (list): Колонки для промежуточных итогов

        Пример:
            >>> report.show_report("name", "hours", group="department")
        """
        ic(self.Meta.model)
        self.sort_records(group, *fields)
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
        """Рассчитывает ширину колонок"""
        for field in self.get_model_fields():
            self._max_lens[field] = max(
                self._max_lens[field],
                len(self._title.get(field, "")) or len(str(field)),
            )

        for record in self._records:
            for key, value in record.items():
                self._max_lens[key] = max(
                    self._max_lens[key],
                    len(str(value)) + len(self._symbol.get("key", "")),
                )

    def __get_update_main_line(self, record: BaseRecordT, *fields: str) -> str:
        """Формирует основную строку"""
        line = " " * self.indent
        for field in fields or self._title.keys():
            if self._title[field] == " ":
                line += "_" * self._max_lens[field]
            else:
                _sym_ = self._symbol.get(field, "")
                line += _sym_ + str(record[field]).ljust(self._max_lens[field])
            line += " " * self.indent
        return line

    def __get_update_group_line(self, record: BaseRecordT) -> str:
        """Обрабатывает группы"""
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
                    _sym_ = self._symbol.get(key, "")
                    line += _sym_ + str(sub_total[key]).ljust(self._max_lens[key])
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

    def set_symbol(self, **symbol: str) -> None:
        """
        Устанавливает символы для форматирования значений

        Параметры:
            **symbols (str): Пары {поле: символ}

        Пример:
            >>> report.set_symbol(price="$", hours="ч")
        """
        for key, value in symbol.items():
            self._symbol[key] = value
