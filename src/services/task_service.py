from typing import List
try:
    from models.todo_list import TodoList  # type: ignore
    from models.task import Task  # type: ignore
    from parsers.task_parser import parse_task_input  # type: ignore
except Exception:  # pragma: no cover
    from ..models.todo_list import TodoList
    from ..models.task import Task
    from ..parsers.task_parser import parse_task_input
from datetime import datetime
try:
    from utils.logger import get_logger  # type: ignore
except Exception:  # pragma: no cover
    from ..utils.logger import get_logger


class TaskService:
    """Facade over `TodoList` with persistence and parsing concerns.

    This class is the orchestrator between the CLI-facing parsing utilities
    and the storage layer. It exposes high-level operations in a cohesive API.
    """

    def __init__(self, storage):
        self.logger = get_logger(__name__)
        self.storage = storage
        self.todo = TodoList()
        self._load()

    def _load(self):
        """Load tasks from storage into the in-memory list."""
        tasks = self.storage.load()
        self.todo.load_tasks(tasks)

    def _persist(self):
        """Persist the in-memory tasks to storage."""
        self.storage.save(self.todo.all_tasks())

    def add(self, raw_input: str) -> Task:
        """Create a new `Task` from raw input and persist it.

        Edge cases:
        - Empty description results in a minimal task with just an id.
        - Invalid fields in the raw input are ignored by the parser.
        """
        parsed = parse_task_input(raw_input)
        task = Task(
            id=0,
            description=parsed["description"],
            tags=parsed["tags"],
            priority=parsed["priority"],
            due_date=parsed["due_date"],
            assigned_to=parsed["assigned_to"],
            time=parsed["time"],
        )
        task = self.todo.add_task(task)
        self._persist()
        self.logger.info("Added task id=%s description=%s", task.id, task.description)
        return task

    def delete(self, task_id: int) -> bool:
        """Delete a task; returns False if the id does not exist."""
        ok = self.todo.delete_task(task_id)
        if ok:
            self._persist()
            self.logger.info("Deleted task id=%s", task_id)
        return ok

    def update(self, task_id: int, raw_input: str) -> bool:
        """Update an existing task with non-null fields from raw input."""
        parsed = parse_task_input(raw_input)

        def updater(t: Task):
            # maybe only override non-null fields
            if parsed["description"]:
                t.description = parsed["description"]
            if parsed["tags"]:
                t.tags = parsed["tags"]
            if parsed["priority"]:
                t.priority = parsed["priority"]
            if parsed["due_date"] is not None:
                t.due_date = parsed["due_date"]
            if parsed["assigned_to"] is not None:
                t.assigned_to = parsed["assigned_to"]
            if parsed["time"] is not None:
                t.time = parsed["time"]
            t.updated_at = datetime.now()

        ok = self.todo.update_task(task_id, updater)
        if ok:
            self._persist()
            self.logger.info("Updated task id=%s", task_id)
        return ok

    def list_all(self) -> List[Task]:
        """Return all tasks."""
        return self.todo.all_tasks()

    def mark_complete(self, task_id: int) -> bool:
        """Mark a task complete and persist."""
        ok = self.todo.mark_complete(task_id)
        if ok:
            self._persist()
            self.logger.info("Marked complete id=%s", task_id)
        return ok

    def mark_incomplete(self, task_id: int) -> bool:
        """Mark a task incomplete and persist."""
        ok = self.todo.mark_incomplete(task_id)
        if ok:
            self._persist()
            self.logger.info("Marked incomplete id=%s", task_id)
        return ok

    def search(self, pattern: str) -> List[Task]:
        """Case-insensitive regex search across description and tags.

        Invalid regex patterns return an empty list instead of raising.
        """
        import re
        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error:
            return []
        return [
            t
            for t in self.todo.all_tasks()
            if (
                regex.search(t.description)
                or any(regex.search(tag) for tag in t.tags)
            )
        ]

    def filter_by_tag(self, tag_pattern: str) -> List[Task]:
        """Return tasks whose tags fully match the given regex pattern."""
        import re
        regex = re.compile(tag_pattern, re.IGNORECASE)
        return [
            t
            for t in self.todo.all_tasks()
            if any(regex.fullmatch(tag) for tag in t.tags)
        ]

    def filter_by_priority(self, prio: str) -> List[Task]:
        """Return tasks with exact priority value."""
        return [t for t in self.todo.all_tasks() if t.priority == prio]

    def filter_by_due(self, date_pattern: str) -> List[Task]:
        """Return tasks whose ISO due date string matches the regex pattern."""
        import re
        regex = re.compile(date_pattern)
        results = []
        for t in self.todo.all_tasks():
            if t.due_date:
                ds = t.due_date.isoformat()
                if regex.search(ds):
                    results.append(t)
        return results
