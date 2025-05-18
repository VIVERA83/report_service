from app.core.utils import arg_parser
from app.report.report import Report

report = Report()


def main():
    result = arg_parser()
    data = report.get_report(
        result.report,
        result.files,
        columns={
            "department": " ",
            "name": "name",
            # "hours_worked": "hours",
            # "hourly_rate": "rate",
            # "payout": "payout",
        },
        subtotal_columns=["hours_worked", "payout"],
        group="department",
    )


if __name__ == "__main__":
    main()
    # python main.py "data/data1.csv" "data/data2.csv" "data/data3.csv" --report payout
