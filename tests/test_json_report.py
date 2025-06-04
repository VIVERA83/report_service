import pytest

from core.record import Record
from data_reporter.report.json import JsonReport


@pytest.fixture
def json_report():
    class TestJsonReport(JsonReport):
        class Meta:
            model = Record

    return TestJsonReport()


def test_json_report_creation(json_report):
    json_report._records = [
        Record(name="Bob", department="IT", hours_worked=100, hourly_rate=60),
        Record(name="Alice", department="IT", hours_worked=10, hourly_rate=60),
    ]
    report = json_report.create_json_report("name", group="department")
    assert "IT" in report
    assert len(report["IT"]["items"]) == 2
