from app.core.setup import Reports
from app.core.utils import args_parser

if __name__ == "__main__":
    result = args_parser()
    report = Reports()
    result = report.handler(result.files, report=result.report)
    if result:
        print(result)
