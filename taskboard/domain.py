import re
from taskboard import storage

class TaskboardError(Exception):
    pass

def add_task(title, db_path):
    trimmed = title.strip()
    if not trimmed:
        raise TaskboardError("Title cannot be blank")
    task = storage.insert_task(trimmed, db_path)
    return task

def list_tasks(db_path):
    return storage.get_all_tasks(db_path)

def complete_task(id_str, db_path):
    try:
        id_int = int(id_str)
    except Exception:
        raise TaskboardError("Invalid task ID")
    if id_int <= 0 or id_int > 9223372036854775807:
        raise TaskboardError("Invalid task ID")
    task = storage.complete_task(id_int, db_path)
    if task is None:
        raise TaskboardError("Task not found")
    return task
