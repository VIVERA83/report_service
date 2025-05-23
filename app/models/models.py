from icecream import ic

from app.models.base import BaseRecord
from app.models.utils import resolve_aliases
from temp.for_check import Payout

HOURLY_RATE = ["hourly_rate", "rate", "salary"]


@resolve_aliases(aliases={"hourly_rate": HOURLY_RATE})
class Record(BaseRecord):

    def post_init(self):
        self["payout"] = self.multiply("hours_worked", "hourly_rate")
