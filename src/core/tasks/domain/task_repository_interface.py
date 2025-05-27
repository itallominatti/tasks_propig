from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

from src.core.tasks.domain.tasks import Task

class TaskRepositoryInterface(ABC):
    @abstractmethod
    def save(self, task: Task) -> None:
        """Save a task to the repository."""
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, task_id: UUID) -> Optional[Task]:
        """Retrieve a task by its ID."""
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, task_id: UUID) -> None:
        """Delete a task by its ID."""
        raise NotImplementedError
    
    @abstractmethod
    def update(self, task: Task) -> None:
        """Update an existing task."""
        raise NotImplementedError
    
    @abstractmethod
    def list(self) -> list[Task]:
        """List all tasks."""
        raise NotImplementedError