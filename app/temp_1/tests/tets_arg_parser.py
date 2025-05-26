from app.core.config import ReportEnum
from app.core.dc import Namespace


def test_report_enum_values():
    assert ReportEnum.to_list() == ["payout", "other"]
    assert isinstance(ReportEnum.payout, ReportEnum)
    assert ReportEnum("payout") == ReportEnum.payout


def test_namespace_dataclass():
    print(1)
    ns = Namespace(files=["test.csv"], report=ReportEnum.other)
    assert ns.files == ["test.csv"]
    assert ns.report == ReportEnum.other
