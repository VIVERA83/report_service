from abc import ABC
from dataclasses import asdict, dataclass
from functools import wraps

from app.core.config import ReportEnum


def resolve_aliases(aliases=None):
    """Декоратор для замены алиасов в аргументах класса"""
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
class BaseRecord(ABC):

    def __init__(self, *_, **__) -> None: ...

    def as_dict(self, *fields: str | None) -> dict:
        if not fields:
            return asdict(self)
        return {key: value for key, value in asdict(self).items() if key in fields}


@dataclass
class Namespace:
    files: list[str]
    report: ReportEnum
