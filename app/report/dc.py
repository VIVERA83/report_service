from dataclasses import dataclass, field

from app.core.dc import BaseRecord, resolve_aliases

HOURLY_RATE = ["hourly_rate", "rate", "salary"]


@resolve_aliases(aliases={"hourly_rate": HOURLY_RATE})
@dataclass(order=True)
class Record(BaseRecord):
    id: str
    name: str
    email: str
    department: str
    hours_worked: int
    hourly_rate: int
    payout: int = field(init=False)

    def __post_init__(self):
        self.hours_worked = int(self.hours_worked)
        self.hourly_rate = int(self.hourly_rate)
        self.payout = self.hours_worked * self.hourly_rate
