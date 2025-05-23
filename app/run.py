from icecream import ic

from app.reports.base import ShowReport, JsonReport
from models.models import Record


class MyReport(ShowReport, JsonReport):
    ...

if __name__ == "__main__":
    report = MyReport(Record)
    files = [
        "../data/data1.csv",
        "../data/data2.csv",
        # "data/data_new.csv"
    ]
    # files = ["data/data1.csv"]
    # report = ShowReport(Record)
    report.load_from_files(*files)
    # print(*report._records, sep="\n")
    # report.sort_records("hours_worked", "name")
    # print()
    # print(*report._records, sep="\n")
    report.set_title_report(
        # name="Фамилия Имя Отчество",
        department=" ",
        hours_worked="Всего часов",
    )
    ic(report.create_json_report())
    ic(
        report.show_report(
            "id",
            "name",
            "email",
            "hours_worked",
            # # #
            # # "department",
            "hourly_rate",
            group="department",
            subtotal_columns=[
                # "hours_worked",
                "hourly_rate"
            ],
        )
    )

# for file in files:
# for dynamic_data in file_parse(file, Record):
#     print(dynamic_data)
#     print(dynamic_data.sort(by="custom", key_func=custom_sort("department", "name", "id")))
#     print(dynamic_data)
#     break
#     # ic(dynamic_data.multiply("hourly_rate", "hours_worked"))
#     # break
