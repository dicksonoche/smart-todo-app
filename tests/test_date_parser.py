import pytest
from parsers.date_parser import parse_due_date
from datetime import datetime, timedelta

def test_iso_date():
    """Parses explicit ISO due date token into the correct date components."""
    d = parse_due_date("due:2025-12-01")
    assert d.year == 2025 and d.month == 12 and d.day == 1

def test_tomorrow():
    """Resolves 'tomorrow' relative to today's date."""
    now = datetime.now()
    d = parse_due_date("due:tomorrow")
    assert (d.date() - now.date()) == timedelta(days=1)

def test_next_week():
    """Resolves 'next week' to approximately seven days ahead."""
    now = datetime.now()
    d = parse_due_date("due:next week")
    assert (d.date() - now.date()).days in range(6, 8)
