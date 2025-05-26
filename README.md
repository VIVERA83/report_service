# Отчетность данных

Проект для генерации отчетов в различных форматах из структурированных данных

## Особенности

- 🗃 **Мультиформатность**:
    - JSON-отчеты для интеграции
    - Красивые консольные таблицы
- 🔍 **Гибкая настройка**:
    - Сортировка по любым полям
    - Группировка данных
    - Промежуточные итоги
- 📊 **Автоматическое форматирование**:
    - Выравнивание колонок
    - Кастомные заголовки
    - Символы форматирования

## Быстрый старт

### Требования

- Python 3.10+
- Зависимости:

```bash
pip install -r requirements.txt
```

### Пример использования

```python
from data_reporter.report.json import JsonReport
from data_reporter.report.show import ShowReport
from data_reporter.record.base import BaseRecord
from core.decorators import resolve_aliases

# Генерация JSON
json_report = JsonReport()
json_report.load_from_files("data.csv")
result = json_report.create_json_report("name", "hours", group="department")

# Консольный вывод
console_report = ShowReport()
console_report.load_from_files("data.csv")
console_report.set_title_report(name="Сотрудник", hours="Часы")
console_report.show_report("name", "hours", group="department")

# Кастомный отчет
HOURLY_RATE = ["hourly_rate", "rate", "salary"]

@resolve_aliases(aliases={"hourly_rate": HOURLY_RATE})
class Record(BaseRecord):
    """
    Специализированный класс для работы с записями о выплатах.

    Особенности:
        - Автоматический расчет поля payout
        - Поддержка псевдонимов для полей (через декоратор resolve_aliases)
    """

    def post_init(self):
        """
        Вычисляет выплату (payout) как произведение часов работы на ставку.
        Вызывается автоматически после инициализации объекта.
        """
        self["payout"] = self.multiply("hours_worked", "hourly_rate")


class ShowPayoutReport(ShowReport):
    class Meta:
        model = Record


console_report = ShowPayoutReport()
console_report.load_from_files("../data/data1.csv")
console_report.set_title_report(
            department=" ",
            hours_worked="hours",
            hourly_rate="rate",
            name="employee"
        )
console_report.set_symbol(payout="Р")
console_report.show_report("name", "hours_worked", "hourly_rate", "payout", group="department")
```
Пример вывода
![img.png](img.png)

