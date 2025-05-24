from typing import TypeVar

from app.models.base import BaseRecord

BaseRecordT = TypeVar("BaseRecordT", bound=BaseRecord)
