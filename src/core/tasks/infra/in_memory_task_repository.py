from uuid import UUID
from typing import Optional, List

from src.core.tasks.domain.task_repository_interface import TaskRepositoryInterface
from src.core.tasks.domain.tasks import Task

class InMemoryTaskRepository(TaskRepositoryInterface):
    """In-memory implementation of the TaskRepositoryInterface."""

    def __init__(self, tasks: Optional[List[Task]] = None) -> None:
        self.tasks = tasks or []

    def save(self, task: Task) -> None:
        """Save a task to the in-memory repository."""
        self.tasks.append(task)

    def get_by_id(self, task_id: UUID) -> Optional[Task]:
        """Retrieve a task by its ID."""
        return next((task for task in self.tasks if task.id == task_id), None)

    def delete(self, task_id: UUID) -> None:
        """Delete a task by its ID."""
        self.tasks = [task for task in self.tasks if task.id != task_id]

    def update(self, task: Task) -> None:
        """Update an existing task."""
        for i, existing_task in enumerate(self.tasks):
            if existing_task.id == task.id:
                self.tasks[i] = task
                break

    def list(self) -> List[Task]:
        """List all tasks."""
        return [task for task in self.tasks]