from enum import Enum
from app.core.reports import JsonReport, ShowReport

class ReportEnum(str, Enum):
    payout = "payout"
    json_payout = "json_payout"

class CLIHandler:
    def __init__(self):
        self.commands = {
            ReportEnum.payout: self.handle_payout,
            ReportEnum.json_payout: self.handle_json_payout
        }

    def handle_payout(self, files):
        report = ShowReport()
        # ... логика отчета
        return report

    def handle_json_payout(self, files):
        report = JsonReport()
        # ... логика отчета
        return report