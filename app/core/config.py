from enum import Enum


class ReportEnum(str, Enum):
    payout = "payout"
    other = "other"

    @classmethod
    def to_list(cls) -> list[str]:
        return list(cls.__members__.keys())
