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
from reports import JsonReport, ShowReport

# Генерация JSON
json_report = JsonReport()
json_report.load_from_files("data.csv")
result = json_report.create_json_report("name", "hours", group="department")

# Консольный вывод
console_report = ShowReport()
console_report.load_from_files("data.csv")
console_report.set_title_report(name="Сотрудник", hours="Часы")
console_report.show_report("name", "hours", group="department")

```
Пример вывода
![img.png](img.png)

