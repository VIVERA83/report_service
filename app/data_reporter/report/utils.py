from typing import Any, Callable


def custom_sort(*fields: str) -> Callable[[tuple[str, Any]], int]:
    """Генерирует функцию для кастомный сортировки."""

    def inner(key) -> int:
        try:
            return fields.index(key)
        except ValueError:
            return len(fields)

    return lambda el: inner(el[0])
