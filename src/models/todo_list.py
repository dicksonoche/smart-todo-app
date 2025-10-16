from typing import List, Optional, Callable
from .task import Task


class TodoList:
    """In-memory collection of tasks with simple ID management."""

    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id = 1

    def load_tasks(self, tasks: List[Task]) -> None:
        """Replace current tasks with provided list and reset next id."""
        self._tasks = tasks
        if tasks:
            self._next_id = max(t.id for t in tasks) + 1

    def all_tasks(self) -> List[Task]:
        """Return a shallow copy of all tasks to prevent external mutation."""
        return list(self._tasks)

    def add_task(self, task: Task) -> Task:
        """Append a new task assigning it a unique incremental id."""
        task.id = self._next_id
        self._next_id += 1
        self._tasks.append(task)
        return task

    def find_by_id(self, tid: int) -> Optional[Task]:
        """Return the task with id or None if not found."""
        for t in self._tasks:
            if t.id == tid:
                return t
        return None

    def delete_task(self, tid: int) -> bool:
        """Delete a task by id returning True if removed."""
        t = self.find_by_id(tid)
        if t:
            self._tasks.remove(t)
            return True
        return False

    def update_task(self, tid: int, update_fn: Callable[[Task], None]) -> bool:
        """Apply updater function to task by id returning True if updated."""
        t = self.find_by_id(tid)
        if not t:
            return False
        update_fn(t)
        return True

    def filter_tasks(self, predicate: Callable[[Task], bool]) -> List[Task]:
        """Return tasks matching predicate."""
        return [t for t in self._tasks if predicate(t)]

    def mark_complete(self, tid: int) -> bool:
        return self.update_task(tid, lambda t: setattr(t, "completed", True))

    def mark_incomplete(self, tid: int) -> bool:
        return self.update_task(tid, lambda t: setattr(t, "completed", False))
