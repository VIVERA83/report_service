from dataclasses import dataclass, field
from functools import wraps

from app.core.dc import BaseRecord

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

            def __init__(self, *args, **kwargs):
                    for key, value in kwargs.items():
                        setattr(cls, field, value)
                    super().__init__(*args, **kwargs)

            # Вызываем оригинальный конструктор
            orig_init(self, *args, **resolved_kwargs)

        cls.__init__ = __init__
        return cls

    return decorator


@resolve_aliases(aliases={"hourly_rate": HOURLY_RATE})
@dataclass(order=True)
class Record(BaseRecord):
   ...

if __name__ == "__main__":
    data = {
        "user": "<NAME>",
    }
    print(Record(**data))
