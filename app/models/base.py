from icecream import ic

from app.models.utils import is_float_number


class BaseRecord(dict):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def sum(self, *fields: str, default: int = 0) -> int | float:
        for field in fields:
            try:
                default += float(self[field])
            except ValueError as e:
                ic(field, e)
        if is_float_number(default):
            return default
        return int(default)

    def multiply(self, *fields: str, default=1) -> int | float:
        for field in fields:
            try:
                default *= float(self[field])
            except ValueError as e:
                ic(field, e)

        if is_float_number(default):
            return default
        return int(default)

    def sort(self, *, by: str = "keys", key_func=None, reverse=False) -> None:
        """
        Сортирует элементы словаря и сохраняет новый порядок.

        Параметры:
        - by: 'keys' (по ключам), 'values' (по значениям), 'custom' (по кастомный функции)
        - key_func: функция для кастомный сортировки (используется при by='custom')
        - reverse: обратный порядок сортировки
        """
        if by == "keys":
            items = sorted(self.items(), key=lambda x: x[0], reverse=reverse)
        elif by == "values":
            items = sorted(self.items(), key=lambda x: x[1], reverse=reverse)
        elif by == "custom" and key_func:
            items = sorted(self.items(), key=key_func, reverse=reverse)
        else:
            raise ValueError("Некорректные параметры сортировки")

        # Очищаем и пересоздаем словарь с новым порядком элементов
        self.clear()
        for k, v in items:
            self[k] = v
