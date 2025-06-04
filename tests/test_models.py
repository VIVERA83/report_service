import pytest

from core.decorators import resolve_aliases
from core.record import Record


@pytest.fixture
def sample_record():
    return Record(
        id="001",
        name="John Doe",
        email="john@example.com",
        department="IT",
        hours_worked=160,
        rate=1500,  # Используем алиас
    )


def test_record_creation(sample_record):
    assert sample_record["hourly_rate"] == 1500
    assert sample_record["payout"] == 160 * 1500


def test_aliases_handling():
    @resolve_aliases(aliases={"test_field": ["alias1", "alias2"]})
    class TestClass(dict):
        pass

    instance = TestClass(alias1=42)
    assert instance["test_field"] == 42


def test_post_init_calculation():
    record = Record(
        hours_worked=120,
        salary=2000,
        **{k: "" for k in ["id", "name", "email", "department"]}
    )
    assert record["payout"] == 120 * 2000
