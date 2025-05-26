from dataclasses import dataclass, field, make_dataclass
from functools import wraps
from typing import Generator, Type

from icecream import ic

ic.includeContext = True


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
            resolved_kwargs = kwargs["dynamic_data"].copy()
            for field, alias_list in aliases.items():
                for alias in alias_list:
                    if alias in resolved_kwargs:
                        resolved_kwargs[field] = resolved_kwargs.pop(alias)
            # Вызываем оригинальный конструктор
            orig_init(self, *args, {"dynamic_data": resolved_kwargs})

        cls.__init__ = __init__
        return cls

    return decorator


class Base:
    def hello(self):
        print("hello")


def dynamic_dataclass(**kwargs)->Base:
    fields = kwargs.pop("fields", {})
    return make_dataclass("DynamicClass", fields.items(), **kwargs, bases=(Base,))

#
# # Создание класса на лету
# DynamicClass = dynamic_dataclass(fields={"name": str, "age": int})
# obj = DynamicClass(name="Alice", age=30)
#
#
# @dataclass
# class DynamicData(dict):
#     __base_field: dict
#
#     def __getattr__(self, name):
#         return self.get(name)
#
#     def __setattr__(self, name, value):
#         if name in self.__annotations__:
#             super().__setattr__(name, value)
#         else:
#             self[name] = value


# dynamic_data: dict = field(default_factory=dict)
#
# def __post_init__(self):
#     # Динамически добавляем атрибуты из словаря
#     ic()
#     self.dynamic_data = {key.lower(): value for key, value in self.dynamic_data.items()}
#     ic(self.dynamic_data)
#     for key, value in self.dynamic_data.items():
#         ic(key)
#         setattr(self, key.lower(), value)


HOURLY_RATE = ["hourly_rate", "rate", "salary"]


@resolve_aliases(aliases={"hourly_rate": HOURLY_RATE})
class Record(Base):
       ...


def file_parse(file_name: str) -> Generator[Base, None, None]:
    with open(file_name, "r", encoding="utf-8") as f:
        keys = f.readline().strip().split(",")
        for line in f:
            string = line.strip().split(",")
            yield dynamic_dataclass(fields={key: type(value) for key, value in zip(keys, string)})



if __name__ == "__main__":
    files = [
        "data/data1.csv",
        "data/data2.csv",
        "data/data_new.csv"
    ]
    for file in files:
        gen = file_parse(file)
        fields = next(gen)
        for dynamic_data in gen:
            dynamic_data.hello()
