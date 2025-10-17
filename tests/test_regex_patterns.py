import re
from parsers.regex_patterns import TAG_PATTERN, PRIORITY_PATTERN, DUE_DATE_PATTERN, ASSIGNED_PATTERN, TIME_PATTERN

def test_tag_pattern():
    """Extracts '@tag' tokens and exposes the tag group."""
    m = TAG_PATTERN.search("do this @home")
    assert m and m.group("tag") == "home"

def test_priority_pattern():
    """Matches case-insensitive #priority tokens and normalizes value."""
    m = PRIORITY_PATTERN.search("something #High")
    assert m and m.group("priority").lower() == "high"

def test_assigned_pattern():
    """Validates 'assigned:' email captures address in 'email' group."""
    m = ASSIGNED_PATTERN.search("assigned:foo@bar.com")
    assert m and m.group("email") == "foo@bar.com"

def test_time_pattern():
    """Parses time expressions like 'at 4:30pm' into hour/min groups."""
    m = TIME_PATTERN.search("meet at 4:30pm")
    assert m and m.group("hour") == "4"
