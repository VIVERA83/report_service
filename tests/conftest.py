import os.path
import sys
from pathlib import Path

import pytest

from app.report.dc import Record
from app.report.payout import Payout

sys.path.append(str(Path(__file__).parent.parent / "app"))


@pytest.fixture
def sample_records():
    return [
        Record(
            id="1",
            name="Alice",
            email="alice@example.com",
            department="IT",
            hours_worked="160",
            hourly_rate="30",
        ),
        Record(
            id="2",
            name="Bob",
            email="bob@example.com",
            department="HR",
            hours_worked="150",
            hourly_rate="25",
        ),
        Record(
            id="3",
            name="Carol Williams",
            email="carol@example.com",
            department="Design",
            hours_worked="170",
            hourly_rate="60",
        ),
    ]


@pytest.fixture
def sample_csv(tmp_path, sample_records):
    files = []
    for i in range(1, 4):
        path = os.path.join(str(Path(__file__).parent), "data", f"data{i}.csv")
        files.append(path)
    return files


@pytest.fixture
def payout_report(sample_csv):
    report = Payout(Record)
    report.load_records(*sample_csv)
    return report
