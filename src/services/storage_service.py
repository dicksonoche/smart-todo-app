import json
from pathlib import Path
from typing import List
try:
    # When imported as top-level module with PYTHONPATH=src
    from models.task import Task  # type: ignore
except Exception:  # pragma: no cover
    # When imported as part of the src package (python -m src.main)
    from ..models.task import Task


class StorageService:
    """Simple JSON file-backed storage for tasks."""

    def __init__(self, filepath: Path):
        # Accept both string and Path inputs for convenience in tests and CLI
        if not isinstance(filepath, Path):
            filepath = Path(filepath)
        self.filepath = filepath
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> List[Task]:
        """Load tasks list from JSON; return empty list if file missing."""
        if not self.filepath.exists():
            return []
        with self.filepath.open("r", encoding="utf-8") as f:
            data = json.load(f)
        try:
            from models.task import Task as T  # type: ignore
        except Exception:  # pragma: no cover
            from ..models.task import Task as T
        return [T.from_dict(d) for d in data]

    def save(self, tasks: List[Task]) -> None:
        """Persist tasks to disk in a stable JSON representation."""
        data = [t.to_dict() for t in tasks]
        with self.filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
