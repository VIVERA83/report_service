from collections import defaultdict
from dataclasses import asdict, dataclass, field
from functools import wraps
from typing import Generator, Type

HOURLY_RATE = ["hourly_rate", "rate", "salary"]

def resolve_aliases(aliases=None):
    """Декоратор для замены алиасов в аргументах класса.

    """
    if aliases is None:
        aliases = {}  # Значение по умолчанию

    def decorator(cls):
        orig_init = cls.__init__

        @wraps(orig_init)
        def __init__(self, *args, **kwargs):
            # Обрабатываем переданные алиасы
            resolved_kwargs = kwargs.copy()
            for field, alias_list in aliases.items():
                for alias in alias_list:
                    if alias in resolved_kwargs:
                        resolved_kwargs[field] = resolved_kwargs.pop(alias)

            # Вызываем оригинальный конструктор
            orig_init(self, *args, **resolved_kwargs)

        cls.__init__ = __init__
        return cls

    return decorator


@dataclass
class BaseRecord:

    def __init__(self, *_, **__) -> None: ...

    def as_dict(self, *fields: str | None) -> dict:
        if not fields:
            return asdict(self)
        return {key: value for key, value in asdict(self).items() if key in fields}

@resolve_aliases(aliases={"hourly_rate": HOURLY_RATE})
@dataclass(order=True)
class Record(BaseRecord):
    id: str
    name: str
    email: str
    department: str
    hours_worked: int
    hourly_rate: int
    payout: int = field(init=False)

    def __post_init__(self):
        self.hours_worked = int(self.hours_worked)
        self.hourly_rate = int(self.hourly_rate)
        self.payout = self.hours_worked * self.hourly_rate


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




class BaseReport:
    def __init__(self, dc: Type["BaseRecord"], indent: int = 3) -> None:
        self._records: list["BaseRecord"] = []
        self._max_lens: dict[str, int] = defaultdict(int)
        self.indent = indent
        self.subtotal_columns = []
        self.group = ""
        self.dc = dc

    def __file_parse(self, file_name: str) -> Generator["BaseRecord", None, None]:
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

class Payout(BaseReport):

    def get_report(
            self,
            columns: dict[str, str] = None,
            subtotal_columns: list[str] = None,
            group: str = None,
    ) -> dict:
        if columns is None:
            columns = {key: key for key in self.dc.__annotations__.keys()}
        if group:
            columns = {group: group, **columns}

        self._update_column_widths(columns)
        self.subtotal_columns = subtotal_columns if subtotal_columns else []
        self.group = group if group is not None else ""
        self.sort_records(*columns.keys())
        report = self.create_json_report(list(columns.keys()))
        self._show_report(columns)
        return report

    def create_json_report(self, columns: list[str]) -> dict:
        report = defaultdict(dict)
        for record in self._records:
            atr = getattr(record, self.group or "", "")
            if not report[atr].get("items"):
                report[atr]["items"] = [
                    self._sort_raw_record(record.as_dict(*columns), columns)
                ]
                for column in self.subtotal_columns:
                    report[atr][column] = getattr(record, column)
            else:
                report[atr]["items"].append(
                    self._sort_raw_record(record.as_dict(*columns), columns)
                )
                for column in self.subtotal_columns:
                    report[atr][column] += getattr(record, column)

        return report

    def _get_title_report(self, columns: dict[str, str] = None) -> str:
        if columns is None:
            columns = self.__get_columns()

        title = ""
        for column_name, new_name in columns.items():
            title += " " * self.indent
            title += new_name.rjust(self._max_lens[column_name])
        return title

    def __get_columns(self) -> dict[str, str]:
        return {field: field for field in self._records[0].__annotations__.keys()}

    def _show_report(
            self,
            columns: dict[str, str] = None,
    ) -> None:

        result: list[str] = [self._get_title_report(columns)]
        self.current_group = ""
        self.subtotal: dict[str, dict[str, int]] = defaultdict(dict)
        self.is_new_group = True

        for record in self._records:
            raw_record = self._sort_raw_record(
                record.as_dict(*columns.keys()), [*columns.keys()]
            )
            main_line = self.__get_update_main_line(raw_record, columns)
            group_line = self.__get_update_group_line(raw_record)
            sub_line = self.__get_update_sub_line(raw_record)
            self.__update_subtotal(raw_record)

            if sub_line:
                result.append(sub_line)
            if group_line:
                result.append(group_line)

            result.append(main_line)
        #
        self.is_new_group = True
        sub_line = self.__get_update_sub_line(self._records[0].as_dict(*columns.keys()))
        result.append(sub_line)
        return print(*result, sep="\n")

    def __get_update_main_line(
            self, record: dict[str, int | str], column: dict[str, str]
    ) -> str:
        line = " " * self.indent
        for key, value in record.items():
            if column[key] == " ":
                line += "_" * self._max_lens[key]
            else:
                line += str(value).ljust(self._max_lens[key])
            line += " " * self.indent
        return line

    def __get_update_group_line(self, record: dict[str, int | str]) -> str:
        if value := record.get(self.group):
            if self.current_group != value:
                self.current_group = value
                self.is_new_group = True
                return " " * self.indent + str(self.current_group)
        return ""

    def __get_update_sub_line(self, record: dict[str, int | str]) -> str:
        if self.is_new_group and len(self.subtotal) > 0:
            self.is_new_group = False
            line = " " * self.indent
            sub_total = [*self.subtotal.values()][-1]
            for key in record.keys():
                if key in self.subtotal_columns:
                    line += str(sub_total[key]).ljust(self._max_lens[key])
                else:
                    line += " " * self._max_lens[key]
                line += " " * self.indent
            return line
        self.is_new_group = False
        return ""

    def __update_subtotal(self, record: dict[str, int | str]):
        for key, value in record.items():
            if key in self.subtotal_columns:
                if not self.subtotal.get(self.current_group):
                    self.subtotal[self.current_group] = defaultdict(int)
                self.subtotal[self.current_group][key] += value

    @staticmethod
    def _sort_raw_record(raw_record: dict, sort_columns: list[str]) -> dict[str, str]:
        sorting_rule = lambda el: sort_columns.index(el[0])
        return {
            key: value for key, value in sorted(raw_record.items(), key=sorting_rule)
        }
