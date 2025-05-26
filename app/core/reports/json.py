from collections import defaultdict

from app.core.reports.base import BaseReport


class JsonReport(BaseReport):
    """
    Класс для генерации структурированных отчетов в JSON-формате

    Наследует:
        BaseReport

    Методы:
        create_json_report(): Формирует отчет с группировкой
    """

    def create_json_report(self, *fields: str, group: str = None) -> dict:
        """
        Создает отчет с возможностью группировки

        Параметры:
            fields (str): Поля для включения в отчет
            group (str): Поле для группировки

        Возвращает:
            dict: Отчет в формате:
                {
                    "group1": {"items": [records]},
                    ...
                }

            Пример:
                >>> report = JsonReport()
                >>> report.load_from_files("data.csv")
                >>> result = report.create_json_report("name", "hours", group="department")
        """
        (
            self.sort_records(group, *fields)
            if group is not None
            else self.sort_records(*fields)
        )
        fields = fields or self.get_model_fields()
        result = defaultdict(dict)
        for report in self._records:
            if data := {key: value for key, value in report.items() if key in fields}:
                if group:
                    arr = result.get(report[group], {"items": []})
                    arr["items"].append(data)
                    result[report[group]] = arr
                else:
                    arr = result.get("items", [])
                    arr.append(data)
                    result["items"] = arr
        return result