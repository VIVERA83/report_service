from icecream import ic
from models.models import Record

from app.reports.base import JsonReport, ShowReport


class MyReport(ShowReport, JsonReport):
    class Meta:
        model = Record


if __name__ == "__main__":
    report = MyReport()
    files = [
        "../data/data1.csv",
        # "../data/data2.csv",
        # "../data/data3.csv"
    ]

    report.load_from_files(*files)

    report.set_title_report(
        department=" ",
        hours_worked="hours",
        hourly_rate="rate",
    )
    report.set_symbol(
        payout="$",
    )
    data = report.create_json_report(

        "department",
        # # "id",
        "name",
        # # "email",
        "hours_worked",
        # # # #
        "hourly_rate",
        "payout",
        group="department",
        # subtotal_columns=[
        #     "hours_worked",
        #     "hourly_rate",
            # "payout",
        # ],
    )
    ic(data)
    ic(
        report.show_report(
            "department",
            # # "id",
            "name",
            # # "email",
            "hours_worked",
            # # # #
            "hourly_rate",
            "payout",
            group="department",
            subtotal_columns=[
                "hours_worked",
                # "hourly_rate",
                "payout",
            ],
        )
    )
