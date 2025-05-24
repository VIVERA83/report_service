import pytest

from app.reports.base import BaseReport
from app.models.base import BaseRecord
from app.models.models import Record
import tempfile


@pytest.fixture
def base_report():
    class TestReport(BaseReport):
        class Meta:
            model = Record

    return TestReport()


def test_load_from_files(base_report):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("id,name,email,department,hours_worked,rate\n")
        f.write("001,John,john@test.com,IT,160,1500")

    base_report.load_from_files(f.name)
    assert len(base_report._records) == 1
    assert base_report._records[0]["name"] == "John"


def test_sort_records(base_report):
    records = [
        Record(name="Bob", department="HR", hours_worked=100, hourly_rate=60),
        Record(name="Alice", department="IT", hours_worked=10, hourly_rate=60)
    ]

    base_report._records = records
    base_report.sort_records("name")

    assert base_report._records[0]["name"] == "Alice"
