from datetime import datetime
from .regex_patterns import (
    TAG_PATTERN,
    PRIORITY_PATTERN,
    DUE_DATE_PATTERN,
    ASSIGNED_PATTERN,
    TIME_PATTERN,
    RECURRENCE_PATTERN,
)
from .date_parser import parse_due_date
from .validator import validate_email


def parse_task_input(text: str) -> dict:
    """Parse a raw input string into structured task fields.

    Returns a mapping with keys: description, tags, priority, due_date,
    assigned_to, time, recurrence. Unknown/invalid tokens are ignored.
    """
    # Extract tags
    tags = [m.group("tag") for m in TAG_PATTERN.finditer(text)]

    # Extract priority (take the first)
    pr_match = PRIORITY_PATTERN.search(text)
    priority = pr_match.group("priority").lower() if pr_match else None

    # Extract due date
    due_match = DUE_DATE_PATTERN.search(text)
    due_date = None
    if due_match:
        due_date = parse_due_date(due_match.group(0))
    else:
        # Fallback: detect natural tokens without prefix
        for candidate in ("tomorrow", "next week"):
            if candidate in text.lower():
                due_date = parse_due_date(candidate)
                break

    # Extract assigned email
    asn_match = ASSIGNED_PATTERN.search(text)
    assigned_to = None
    if asn_match:
        email = asn_match.group("email")
        if validate_email(email):
            assigned_to = email

    # Extract time
    tm_match = TIME_PATTERN.search(text)
    time = None
    if tm_match:
        hour = int(tm_match.group("hour"))
        minute = int(tm_match.group("minute") or 0)
        ampm = tm_match.group("ampm")
        if ampm:
            ampm = ampm.lower()
            if ampm == "pm" and hour < 12:
                hour += 12
            elif ampm == "am" and hour == 12:
                hour = 0
        # combine with date (due_date or today)
        base_date = due_date or datetime.now()
        time = base_date.replace(
            hour=hour, minute=minute, second=0, microsecond=0
        )

    # Extract recurrence (optional)
    rec_match = RECURRENCE_PATTERN.search(text)
    recurrence = rec_match.group("interval").lower() if rec_match else None

    # Now strip out parsed tokens to get “clean” description
    # (very naive: you can refine)
    cleaned = text
    # remove tag tokens
    cleaned = TAG_PATTERN.sub("", cleaned)
    cleaned = PRIORITY_PATTERN.sub("", cleaned)
    cleaned = DUE_DATE_PATTERN.sub("", cleaned)
    cleaned = ASSIGNED_PATTERN.sub("", cleaned)
    cleaned = TIME_PATTERN.sub("", cleaned)
    cleaned = RECURRENCE_PATTERN.sub("", cleaned)
    description = cleaned.strip().strip('"').strip()

    return {
        "description": description,
        "tags": tags,
        "priority": priority,
        "due_date": due_date,
        "assigned_to": assigned_to,
        "time": time,
        "recurrence": recurrence,
    }
