from app.models.utils import is_float_number


class BaseRecord(dict):
    """
        Расширенный словарь с дополнительными операциями над данными.

        Наследует:
            dict

        Методы:
            post_init(): Дополнительная инициализация после создания объекта
            sum(): Вычисляет сумму указанных полей
            multiply(): Вычисляет произведение указанных полей
            sort(): Сортирует элементы словаря
        """

    def __init__(self, *args, **kwargs) -> None:
        """
            Инициализация объекта. После стандартной инициализации словаря
            вызывает метод post_init() для дополнительной настройки.
        """
        super().__init__(*args, **kwargs)
        self.post_init()

    def post_init(self):
        """
            Шаблонный метод для дополнительной инициализации.
            Может быть переопределен в дочерних классах.
        """

    def sum(self, *fields: str, default: int = 0) -> int | float:
        """
            Вычисляет сумму значений указанных полей.

            Параметры:
                fields: Список имен полей для суммирования
                default: Начальное значение суммы (по умолчанию 0)

            Возвращает:
                Сумма значений в виде int или float

            Пример:
                >>> record = BaseRecord(a=10, b=20.5)
                >>> record.sum('a', 'b')
                30.5
        """
        for field in fields:
            try:
                default += float(self[field])
            except ValueError as e:
                print(field, e)
        if is_float_number(default):
            return default
        return int(default)

    def multiply(self, *fields: str, default=1) -> int | float:
        """
            Вычисляет произведение значений указанных полей.

            Параметры:
                fields: Список имен полей для перемножения
                default: Начальное значение (по умолчанию 1)

            Возвращает:
                Произведение значений в виде int или float

            Пример:
                >>> record = BaseRecord(x=2, y=3.5)
                >>> record.multiply('x', 'y')
                7.0
        """
        for field in fields:
            try:
                default *= float(self[field])
            except ValueError as e:
                print(field, e)

        if is_float_number(default):
            return default
        return int(default)

    def sort(self, *, by: str = "keys", key_func=None, reverse=False) -> None:
        """
        Сортирует элементы словаря с возможностью выбора стратегии сортировки.

        Параметры:
            by: Критерий сортировки:
                - 'keys' (по ключам)
                - 'values' (по значениям)
                - 'custom' (по пользовательской функции)
            key_func: Функция для кастомной сортировки (требуется при by='custom')
            reverse: Обратный порядок сортировки

        Исключения:
            ValueError: При некорректных параметрах сортировки

        Пример:
            >>> d = BaseRecord(b=2, a=1)
            >>> d.sort(by='keys')
            >>> d
            {'a': 1, 'b': 2}
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
