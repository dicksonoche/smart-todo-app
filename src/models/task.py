from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class Task:
    """A single to-do item with optional metadata.

    Fields are intentionally simple to keep persistence straightforward.
    Time- and date-only fields are stored as naive datetimes in local time.
    """
    id: int
    description: str
    tags: List[str] = field(default_factory=list)
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None
    time: Optional[datetime] = None
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the task into a JSON-safe dictionary."""
        return {
            "id": self.id,
            "description": self.description,
            "tags": self.tags,
            "priority": self.priority,
            "due_date": (
                self.due_date.isoformat() if self.due_date else None
            ),
            "assigned_to": self.assigned_to,
            "time": (
                self.time.isoformat() if self.time else None
            ),
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> Task:
        """Create a Task from a dictionary previously produced by to_dict."""
        if d.get("due_date"):
            due = datetime.fromisoformat(d["due_date"])
        else:
            due = None

        if d.get("time"):
            time = datetime.fromisoformat(d["time"])
        else:
            time = None
        return Task(
            id=d["id"],
            description=d["description"],
            tags=d.get("tags", []),
            priority=d.get("priority"),
            due_date=due,
            assigned_to=d.get("assigned_to"),
            time=time,
            completed=d.get("completed", False),
            created_at=(
                datetime.fromisoformat(d["created_at"]) if d.get("created_at") else datetime.now()
            ),
            updated_at=(
                datetime.fromisoformat(d["updated_at"]) if d.get("updated_at") else datetime.now()
            ),
        )
