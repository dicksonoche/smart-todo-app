import tempfile
import os
import json
from services.storage_service import StorageService
from services.task_service import TaskService

def test_add_and_persist(tmp_path):
    """Adds a task, persists to disk, and reloads into a fresh service."""
    filepath = tmp_path / "tasks.json"
    storage = StorageService(filepath)
    svc = TaskService(storage)

    t = svc.add('Test one @tag1 #low due:2025-11-11 assigned:bob@example.com')
    assert t.id == 1
    assert t.description.startswith("Test one")

    # reload into new service
    svc2 = TaskService(StorageService(filepath))
    all_tasks = svc2.list_all()
    assert len(all_tasks) == 1
    assert all_tasks[0].description == t.description

def test_delete():
    """Deletes an existing task and returns an empty list after removal."""
    storage = StorageService(tmp_path := tempfile.TemporaryDirectory().name)
    svc = TaskService(storage)
    t = svc.add("A task")
    assert svc.delete(t.id)
    assert svc.list_all() == []
