import pytest
from argparse import ArgumentError

from service.cli import create_name_space
from service.cli.commands import ReportEnum
from service.cli.parser import CLINamespace


def test_create_namespace_valid_args(monkeypatch):
    """Тест корректных аргументов"""
    test_args = ["file1.csv", "file2.csv", "--report", "payout"]
    monkeypatch.setattr("sys.argv", ["prog"] + test_args)

    result = create_name_space()

    assert isinstance(result, CLINamespace)
    assert result.files == ["file1.csv", "file2.csv"]
    assert result.report == "payout"


def test_missing_report_arg(monkeypatch):
    """Тест отсутствия обязательного аргумента --report"""
    test_args = ["file1.csv"]
    monkeypatch.setattr("sys.argv", ["prog"] + test_args)

    with pytest.raises((ArgumentError, SystemExit)):
        create_name_space()


def test_invalid_report_value(monkeypatch):
    """Тест недопустимого значения отчета"""
    test_args = ["file1.csv", "--report", "invalid_report"]
    monkeypatch.setattr("sys.argv", ["prog"] + test_args)

    with pytest.raises((ArgumentError, SystemExit)):
        create_name_space()


def test_no_files_provided(monkeypatch):
    """Тест отсутствия файлов"""
    test_args = ["--report", "payout"]
    monkeypatch.setattr("sys.argv", ["prog"] + test_args)

    with pytest.raises((ArgumentError, SystemExit)):
        create_name_space()


def test_namespace_dataclass():
    """Проверка структуры CLINamespace"""
    ns = CLINamespace(files=["data.csv"], report="json_payout")
    assert ns.files == ["data.csv"]
    assert ns.report == "json_payout"
    assert isinstance(ns, CLINamespace)


def test_report_enum_compatibility():
    """Проверка совместимости с ReportEnum"""
    valid_reports = ReportEnum.to_list()
    assert "payout" in valid_reports
    assert "json_payout" in valid_reports
    assert len(valid_reports) == 2
