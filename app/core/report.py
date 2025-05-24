from app.models.models import Record
from app.reports.base import ShowReport, JsonReport



class ShowPayoutReport(ShowReport):
    class Meta:
        model = Record

class JsonPayoutReport(JsonReport):
    class Meta:
        model = Record
