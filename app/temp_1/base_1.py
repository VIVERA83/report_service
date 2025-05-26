from functools import wraps
from typing import Generator

from icecream import ic

HOURLY_RATE = ["hourly_rate", "rate", "salary"]


# def resolve_aliases(aliases=None):
#     """Декоратор для замены алиасов в аргументах класса.
#
#     """
#     if aliases is None:
#         aliases = {}  # Значение по умолчанию
#
#     def decorator(cls):
#         orig_init = cls.__init__
#
#         @wraps(orig_init)
#         def __init__(self, *args, **kwargs):
#             # Обрабатываем переданные алиасы
#             resolved_kwargs = kwargs.copy()
#             for field, alias_list in aliases.items():
#                 for alias in alias_list:
#                     if alias in resolved_kwargs:
#                         resolved_kwargs[field] = resolved_kwargs.pop(alias)
#             # Вызываем оригинальный конструктор
#             orig_init(self, *args, **resolved_kwargs)
#
#         cls.__init__ = __init__
#         return cls
#
#     return decorator


# class DynamicClass(dict):
#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)
#
#     def sum(self, *fields: str, default: int = 0) -> int | float:
#         for field in fields:
#             try:
#                 default += float(self[field])
#             except ValueError as e:
#                 ic(field, e)
#         if is_float(default):
#             return default
#         return int(default)
#
#     def multiply(self, *fields: str, default=1) -> int | float:
#         for field in fields:
#             try:
#                 default *= float(self[field])
#             except ValueError as e:
#                 ic(field, e)
#
#         if is_float(default):
#             return default
#         return int(default)
#
#     def sort(self, *, by: str = 'keys', key_func=None, reverse=False) -> None:
#         """
#         Сортирует элементы словаря и сохраняет новый порядок.
#
#         Параметры:
#         - by: 'keys' (по ключам), 'values' (по значениям), 'custom' (по кастомный функции)
#         - key_func: функция для кастомный сортировки (используется при by='custom')
#         - reverse: обратный порядок сортировки
#         """
#         if by == 'keys':
#             items = sorted(self.items(), key=lambda x: x[0], reverse=reverse)
#         elif by == 'values':
#             items = sorted(self.items(), key=lambda x: x[1], reverse=reverse)
#         elif by == 'custom' and key_func:
#             items = sorted(self.items(), key=key_func, reverse=reverse)
#         else:
#             raise ValueError("Некорректные параметры сортировки")
#
#         # Очищаем и пересоздаем словарь с новым порядком элементов
#         self.clear()
#         for k, v in items:
#             self[k] = v


# def is_float(number: int | float) -> bool:
#     integer = int(number)
#     return ic((integer / 2) * 2 != number)


@resolve_aliases(aliases={"hourly_rate": HOURLY_RATE})
class Record(DynamicClass):
    ...

#
# def file_parse(file_name: str) -> Generator[DynamicClass, None, None]:
#     with open(file_name, "r", encoding="utf-8") as f:
#         keys = f.readline().strip().split(",")
#         for line in f:
#             string = line.strip().split(",")
#             yield Record(**{ic(key): ic(value) for key, value in zip(keys, string)})
#
#
# def custom_sort(*fields: str):
#     def inner(key):
#         try:
#             return fields.index(key)
#         except ValueError:
#             return len(fields)
#
#     return lambda el: inner(el[0])


if __name__ == "__main__":
    files = [
        "data/data1.csv",
        # "data/data2.csv",
        # "data/data_new.csv"
    ]
    for file in files:
        for dynamic_data in file_parse(file):
            print(dynamic_data)
            print(dynamic_data.sort(by="custom", key_func=custom_sort("department", "name", "id")))
            print(dynamic_data)
            break
            # ic(dynamic_data.multiply("hourly_rate", "hours_worked"))
            # break
