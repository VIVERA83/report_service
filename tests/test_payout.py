import pytest
from io import StringIO
import sys

from app.report.dc import Record
from app.report.payout import Payout
from app.core.config import ReportEnum
from app.core.dc import Namespace


def test_record_creation(sample_records):
    record = sample_records[0]
    assert record.id == "1"
    assert record.payout == 160 * 30
    assert isinstance(record.hours_worked, int)
    assert isinstance(record.hourly_rate, int)


def test_record_as_dict(sample_records):
    record = sample_records[0]
    d = record.as_dict()
    assert d["id"] == "1"
    assert d["payout"] == 4800
    assert "email" in d


# Тесты для BaseReport
def test_load_records(payout_report):
    assert len(payout_report._records) == 9
    assert isinstance(payout_report._records[0], Record)


def test_column_widths_calculation(payout_report):
    assert payout_report._max_lens["name"] == len("Carol Williams")
    assert payout_report._max_lens["payout"] == len(str(180 * 35 * 2))


def test_sorting_records(payout_report):
    payout_report.sort_records("department", "name")
    departments = [r.department for r in payout_report._records]
    assert departments == [
        "Design",
        "Design",
        "HR",
        "HR",
        "HR",
        "Marketing",
        "Marketing",
        "Sales",
        "Sales",
    ]


# Тесты для Payout
def test_json_report_structure(payout_report):
    report = payout_report.get_report(
        columns={"name": "Employee", "payout": "Salary"},
        subtotal_columns=["payout"],
        group="department",
    )

    assert "HR" in report
    assert len(report["HR"]["items"]) == 3
    assert report["HR"]["payout"] == sum(
        r.payout for r in payout_report._records if r.department == "HR"
    )


def test_report_output_formatting(payout_report, monkeypatch):
    captured = StringIO()
    monkeypatch.setattr(sys, "stdout", captured)

    payout_report.get_report(
        columns={"name": "Employee", "hours_worked": "Hours"},
        subtotal_columns=["hours_worked"],
    )

    output = captured.getvalue()
    assert "Employee" in output
    assert "Hours" in output
    assert str(160) in output


def test_subtotal_calculation(payout_report):
    report = payout_report.get_report(
        columns={"name": "Employee"}, subtotal_columns=["payout"], group="department"
    )

    design_total = sum(
        r.payout for r in payout_report._records if r.department == "Design"
    )
    hr_total = sum(r.payout for r in payout_report._records if r.department == "HR")
    assert report["Design"]["payout"] == design_total
    assert report["HR"]["payout"] == hr_total


def test_edge_cases(tmp_path):
    empty_file = tmp_path / "empty.csv"
    empty_file.touch()

    report = Payout(Record)
    report.load_records(str(empty_file))
    assert len(report._records) == 0


def test_grouping_logic(payout_report):
    report = payout_report.get_report(columns={"name": "Employee"}, group="department")

    groups = list(report.keys())
    assert sorted(groups) == ["Design", "HR", "Marketing", "Sales"]


def test_column_ordering(payout_report):
    columns = {"email": "Email", "name": "Name"}
    report = payout_report.create_json_report(list(columns.keys()))

    for group in report.values():
        for item in group["items"]:
            assert list(item.keys()) == ["email", "name"]


def test_report_enum_values():
    assert ReportEnum.to_list() == ["payout", "other"]
    assert isinstance(ReportEnum.payout, ReportEnum)
    assert ReportEnum("payout") == ReportEnum.payout


def test_namespace_dataclass():
    print(1)
    ns = Namespace(files=["test.csv"], report=ReportEnum.other)
    assert ns.files == ["test.csv"]
    assert ns.report == ReportEnum.other


if __name__ == "__main__":
    pytest.main(["-v", __file__])
