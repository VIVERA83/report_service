from enum import Enum

from core.report import ShowPayoutReport, JsonPayoutReport


class ReportEnum(str, Enum):
    payout = "payout"
    json_payout = "json_payout"

    @classmethod
    def to_list(cls) -> list[str]:
        """Возвращает список отчетов."""

        return list(cls.__members__.keys())


class CLIHandler:
    def __init__(self):
        self.commands = {
            ReportEnum.payout: self.handle_payout,
            ReportEnum.json_payout: self.handle_json_payout,
        }

    def handle_payout(self, files):
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

    def handle_json_payout(self, files: str) -> dict:
        report = JsonPayoutReport()
        report.load_from_files(*files)
        return report.create_json_report()
