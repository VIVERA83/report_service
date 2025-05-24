import argparse
from dataclasses import dataclass

from app.core.setup import ReportEnum


@dataclass
class Namespace:
    files: list[str]
    report: str


def args_parser() -> Namespace:
    parser = argparse.ArgumentParser(description="Обработка данных и генерация отчета")
    parser.add_argument(
        "files",
        nargs="+",  # Принимаем один или несколько файлов
        help="Список CSV-файлов для обработки",
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=ReportEnum.to_list(),  # Допустимые значения
        help="Тип генерируемого отчета",
    )

    args = parser.parse_args()

    return Namespace(files=args.files, report=args.report)
