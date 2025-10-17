import pytest
from parsers.validator import validate_email, validate_priority, validate_tag

def test_valid_email():
    """Accepts a correctly formed email address."""
    assert validate_email("alice@example.com")

def test_invalid_email():
    """Rejects an invalid email string."""
    assert not validate_email("not-an-email")

def test_priority():
    """Validates allowed priorities and rejects unknown values."""
    assert validate_priority("high")
    assert validate_priority("medium")
    assert not validate_priority("urgent")

def test_tag():
    """Validates allowed tag token content (no spaces)."""
    assert validate_tag("work")
    assert not validate_tag("with spaces")
