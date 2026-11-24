from threading import Lock
from typing import TypedDict


class Task(TypedDict):
    id: int
    title: str
    description: str
    completed: bool


_tasks: dict[int, Task] = {}
_next_id = 1
_lock = Lock()


def reset_store() -> None:
    global _next_id
    with _lock:
        _tasks.clear()
        _next_id = 1


def list_tasks() -> list[Task]:
    with _lock:
        return [task.copy() for task in _tasks.values()]


def get_task(task_id: int) -> Task | None:
    with _lock:
        task = _tasks.get(task_id)
        return task.copy() if task else None


def create_task(title: str, description: str = "") -> Task:
    clean_title = title.strip()
    if not clean_title:
        raise ValueError("El título no puede estar vacío.")

    global _next_id
    with _lock:
        task: Task = {
            "id": _next_id,
            "title": clean_title,
            "description": description.strip(),
            "completed": False,
        }
        _tasks[_next_id] = task
        _next_id += 1
        return task.copy()


def update_task(task_id: int, title: str, description: str = "") -> Task | None:
    clean_title = title.strip()
    if not clean_title:
        raise ValueError("El título no puede estar vacío.")

    with _lock:
        task = _tasks.get(task_id)
        if task is None:
            return None
        task["title"] = clean_title
        task["description"] = description.strip()
        return task.copy()


def delete_task(task_id: int) -> bool:
    with _lock:
        return _tasks.pop(task_id, None) is not None


def toggle_task(task_id: int) -> Task | None:
    with _lock:
        task = _tasks.get(task_id)
        if task is None:
            return None
        task["completed"] = not task["completed"]
        return task.copy()
