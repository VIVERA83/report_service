from core.record import Record
from data_reporter.report.json import JsonReport
from data_reporter.report.show import ShowReport


class ShowPayoutReport(ShowReport):
    class Meta:
        model = Record


class JsonPayoutReport(JsonReport):
    class Meta:
        model = Record
