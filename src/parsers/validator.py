from .regex_patterns import ASSIGNED_PATTERN, PRIORITY_PATTERN, TAG_PATTERN


def validate_email(email: str) -> bool:
    """Validate email address using the assigned regex.

    Note: This is a pragmatic validator leveraging the same pattern used
    in parsing.
    """
    return bool(ASSIGNED_PATTERN.fullmatch(f"assigned:{email}"))


def validate_priority(priority: str) -> bool:
    """Validate that priority is one of high/medium/low (case-insensitive)."""
    return bool(PRIORITY_PATTERN.fullmatch(f"#{priority}"))


def validate_tag(tag: str) -> bool:
    """Validate that a tag token contains only allowed characters."""
    return bool(TAG_PATTERN.fullmatch(f"@{tag}"))


def validate_date(date_str: str) -> bool:
    """Validate an ISO date string (YYYY-MM-DD or full ISO datetime)."""
    try:
        from datetime import datetime
        datetime.fromisoformat(date_str)
        return True
    except Exception:
        return False


def validate_task_id(task_id: int) -> bool:
    """Validate task id format: positive integer."""
    try:
        return isinstance(task_id, int) and task_id > 0
    except Exception:
        return False
