from dataclasses import dataclass
from uuid import UUID
from typing import Optional
from src.core.tasks.domain.task_repository_interface import TaskRepositoryInterface
from src.core.tasks.application.exceptions import TaskNotFound
from src.core.tasks.domain.tasks import TaskStatus

class UpdateTask:
    def __init__(self, repository: TaskRepositoryInterface) -> None:
        self.repository = repository

    @dataclass
    class UpdateTaskRequest:
        task_id: UUID
        title: Optional[str] = None
        description: Optional[str] = None
        status: Optional[TaskStatus] = None

    def execute(self, request: UpdateTaskRequest) -> None:
        task = self.repository.get_by_id(request.task_id)
        if not task:
            raise TaskNotFound(f"Task with ID {request.task_id} not found.")

        if request.title is not None:
            task.title = request.title
        if request.description is not None:
            task.description = request.description
        if request.status is not None:
            task.status = request.status

        self.repository.save(task)