from uuid import UUID
from dataclasses import dataclass

from src.core.tasks.domain.task_repository_interface import TaskRepositoryInterface
from src.core.tasks.application.exceptions import TaskNotFound

class DeleteTask:
    def __init__(self, repository: TaskRepositoryInterface) -> None:
        self.repository = repository
    
    @dataclass
    class DeleteTaskRequest:
        id: UUID

    def execute(self, request: DeleteTaskRequest) -> None:
        task = self.repository.get_by_id(str(request.id))
        if not task:
            raise TaskNotFound(f"Task with ID {request.id} not found.")
        
        self.repository.delete(str(request.id))