import pytest

from core.record import Record
from data_reporter.report.show import ShowReport


@pytest.fixture
def show_report():
    class TestShowReport(ShowReport):
        class Meta:
            model = Record

    return TestShowReport()


def test_show_report_output(show_report, capsys):
    show_report._records = [
        Record(department="IT", name="John", hours_worked=160, hourly_rate=1500)
    ]
    show_report.set_title_report(name="Employee")
    show_report.show_report("name", "hours_worked")

    captured = capsys.readouterr()
    assert "Employee" in captured.out
    assert "160" in captured.out
