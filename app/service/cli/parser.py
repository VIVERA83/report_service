from dataclasses import dataclass
import argparse

from service.cli.commands import ReportEnum


@dataclass
class CLINamespace:
    files: list[str]
    report: str


def create_parser():
    parser = argparse.ArgumentParser(description="Обработка данных и генерация отчета")
    parser.add_argument(
        "files",
        nargs="+",
        help="Список CSV-файлов для обработки",
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=ReportEnum.to_list(),  # Допустимые значения
        help="Тип генерируемого отчета",
    )
    return parser
