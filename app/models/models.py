from app.models.base import BaseRecord
from app.models.utils import resolve_aliases

HOURLY_RATE = ["hourly_rate", "rate", "salary"]


@resolve_aliases(aliases={"hourly_rate": HOURLY_RATE})
class Record(BaseRecord):

    def post_init(self):
        self["payout"] = self.multiply("hours_worked", "hourly_rate")
