from enum import Enum

from app.core.report import JsonPayoutReport, ShowPayoutReport


class ReportEnum(str, Enum):
    """Список отчетов.

    Сюда добавляем новый тип отчета.
    """

    payout = "payout"
    json_payout = "json_payout"

    @classmethod
    def to_list(cls) -> list[str]:
        """Возвращает список отчетов."""

        return list(cls.__members__.keys())


class Reports:
    def __init__(self):
        self.reports = {
            "payout": payout,
            "json_payout": json_payout,

        }

    def handler(self, files: list[str], report: str):
        if handler := self.reports.get(report):
            return handler(*files)
        else:
            return "не найден"


def payout(*files: str):
    report = ShowPayoutReport()
    report.load_from_files(*files)
    report.set_symbol(
        payout="$",
    )
    report.set_title_report(
        department=" ",
        hours_worked="hours",
        hourly_rate="rate",
    )
    report.show_report(
        "department",
        "name",
        "hours_worked",
        "hourly_rate",
        "payout",
        group="department",
        subtotal_columns=[
            "hours_worked",
            "hourly_rate",
            "payout",
        ],
    )
    return


def json_payout(*files: str) -> dict:
    report = JsonPayoutReport()
    report.load_from_files(*files)
    return report.create_json_report(

    )
