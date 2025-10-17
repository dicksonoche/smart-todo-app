from datetime import datetime, timedelta


def parse_due_date(token: str) -> datetime | None:
    """
    Interpret due date tokens in multiple forms:
    - "due:YYYY-MM-DD"
    - "due:tomorrow" / "due:next week"
    - "YYYY-MM-DD" (no prefix)
    - "tomorrow" / "next week" (no prefix)
    Returns a datetime at midnight for date-only inputs.
    """
    if not token:
        return None

    val = token.strip()
    if val.lower().startswith("due:"):
        val = val.split(":", 1)[1]
    val = val.strip().lower()

    today = datetime.now()
    if val == "tomorrow":
        return (today + timedelta(days=1))
    if val == "next week":
        return (today + timedelta(weeks=1))

    # YYYY-MM-DD
    try:
        return datetime.fromisoformat(val)
    except ValueError:
        return None
