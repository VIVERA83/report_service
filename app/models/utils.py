from functools import wraps
from typing import Any, Callable


def resolve_aliases(aliases=None):
    """Декоратор для замены алиасов в аргументах класса."""

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


def custom_sort(*fields: str) -> Callable[[tuple[str, Any]], int]:
    """Генерирует функцию для кастомный сортировки."""

    def inner(key) -> int:
        try:
            return fields.index(key)
        except ValueError:
            return len(fields)

    return lambda el: inner(el[0])


def is_float_number(number: int | float) -> bool:
    integer = int(number)
    return (integer / 2) * 2 != number
