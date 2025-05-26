from functools import wraps


def resolve_aliases(aliases=None):
    """Декоратор для обработки псевдонимов полей класса.

    Args:
        aliases: Словарь псевдонимов в формате {поле: [список_псевдонимов]}
    """

    def decorator(cls):
        orig_init = cls.__init__

        @wraps(orig_init)
        def wrapped_init(self, *args, **kwargs):
            resolved_kwargs = kwargs.copy()
            for field, alias_list in (aliases or {}).items():
                for alias in alias_list:
                    if alias in resolved_kwargs:
                        resolved_kwargs[field] = resolved_kwargs.pop(alias)
            orig_init(self, *args, **resolved_kwargs)

        cls.__init__ = wrapped_init
        return cls

    return decorator