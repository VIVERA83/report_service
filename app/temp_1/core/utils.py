import argparse

from app.core.config import ReportEnum
from app.core.dc import Namespace


def arg_parser() -> Namespace:
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
