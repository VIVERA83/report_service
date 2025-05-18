from typing import Any

from app.report.base import BaseReport
from app.report.dc import Record
from app.report.payout import Payout


class Report:
    def __init__(self):
        self.reports: dict[str, BaseReport] = {"payout": Payout(Record)}

    def get_report(
        self,
        report: str,
        files: list[str],
        columns: dict[str, str] = None,
        subtotal_columns: list[str] = None,
        group: str = None,
    ) -> dict[str, Any]:
        report = self.reports[report]
        report.load_records(*files)
        if columns is None:
            columns = {key: key for key in report.dc.__annotations__.keys()}
        if group:
            columns = {
                group: group, **columns,
            }
        if subtotal_columns:
            for column in subtotal_columns:
                if not columns.get(column):
                    columns[column] = column

        return report.get_report(
            columns,
            subtotal_columns,
            group,
        )
