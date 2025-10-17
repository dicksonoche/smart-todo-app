import pytest
from parsers.task_parser import parse_task_input

def test_parse_basic():
    """Parses basic input extracting description, tags, priority, email, due."""
    raw = 'Buy groceries @shopping #high due:2025-10-20 assigned:alice@example.com'
    res = parse_task_input(raw)
    assert res["description"].startswith("Buy groceries")
    assert "shopping" in res["tags"]
    assert res["priority"] == "high"
    assert res["assigned_to"] == "alice@example.com"
    assert res["due_date"] is not None

def test_parse_time():
    """Anchors parsed time to due date (or today) for a concrete datetime."""
    raw = 'Call mom tomorrow at 3pm @family'
    res = parse_task_input(raw)
    assert "family" in res["tags"]
    assert res["time"] is not None
    assert res["due_date"] is not None
