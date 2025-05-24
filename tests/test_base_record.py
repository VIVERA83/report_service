from app.models.base import BaseRecord


def test_sum_calculation():
    record = BaseRecord(a=10, b=20.5)
    assert record.sum("a", "b") == 30.5


def test_sort_functionality():
    record = BaseRecord(b=2, a=1)
    record.sort(by="keys")
    assert list(record.keys()) == ["a", "b"]
