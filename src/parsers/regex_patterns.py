import re

# Tag: @tagName (alphanumeric + underscores)
TAG_PATTERN = re.compile(r"@(?P<tag>[A-Za-z0-9_]+)")

# Priority: #high, #medium, #low (case-insensitive)
PRIORITY_PATTERN = re.compile(r"#(?P<priority>high|medium|low)", re.IGNORECASE)

# Due: due:YYYY-MM-DD or due:tomorrow or due:next week
DUE_DATE_PATTERN = re.compile(
    r"due:(?P<due>(\d{4}-\d{2}-\d{2}|tomorrow|next week))", re.IGNORECASE
)

# Assigned: email address
ASSIGNED_PATTERN = re.compile(
    r"assigned:(?P<email>[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+)"
)

# Time: “at 3pm”, “by 5:30 PM”
TIME_PATTERN = re.compile(
    r"(?:(?:at|by)\s*)(?P<hour>\d{1,2})(?::(?P<minute>\d{2}))?\s*"
    r"(?P<ampm>am|pm|AM|PM)?"
)

# Recurrence (optional): e.g. “every Monday”, “every day”
RECURRENCE_PATTERN = re.compile(r"every\s+(?P<interval>\w+)", re.IGNORECASE)
