from uuid import UUID
from dataclasses import dataclass, field
from typing import Dict, Any, Set

from src.core.tasks.application.exceptions import TaskNotFound
from src.core.tasks.domain.task_repository_interface import TaskRepositoryInterface

@dataclass
class TaskOutput:
    id: UUID
    title: str
    description: str
    status: str
    created_at: str
    updated_at: str
    users: Set[UUID]
    links: Dict[str, Any] = field(default_factory=dict)

class GetTask:
    @dataclass
    class GetTaskRequest:
        task_id: UUID

    @dataclass
    class GetTaskResponse:
        data: TaskOutput
        links: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, repository: TaskRepositoryInterface) -> None:
        self.repository = repository

    def execute(self, request: GetTaskRequest) -> GetTaskResponse:
        task = self.repository.get_by_id(request.task_id)
        if not task:
            raise TaskNotFound(f"Task with ID {request.task_id} not found.")

        task_output = TaskOutput(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat(),
            users=set(task.users),
            links={
                "self": f"/api/tasks/{task.id}",
                "create": {
                    "methods": ["POST", "OPTIONS", "HEAD"],
                    "href": "/api/tasks",
                    "description": (
                        "Create a new task. "
                        "POST expects: title (string), description (string, optional), users ([UUID], optional). "
                        "OPTIONS returns allowed methods and metadata. "
                        "HEAD returns headers only."
                    ),
                    "body": {
                        "title": "string",
                        "description": "string (optional)",
                        "users": "[UUID] (optional, default is yourself)"
                    }
                },
                "delete": {
                    "method": "DELETE",
                    "href": f"/api/tasks/{task.id}",
                    "description": "Delete the task."
                },
                "update": {
                    "method": "PUT",
                    "href": f"/api/tasks/{task.id}",
                    "description": "Update the task.",
                    "body": {
                        "title": "string",
                        "description": "string (optional)",
                        "users": "[UUID] (optional, default is yourself)"
                    }
                },
                "patch": {
                    "method": "PATCH",
                    "href": f"/api/tasks/{task.id}",
                    "description": "Partially update the task.",
                    "body": {
                        "title": "string (optional)",
                        "description": "string (optional)",
                        "users": "[UUID] (optional, default is yourself)"
                    }
                }
            }
        )

        return self.GetTaskResponse(
            data=task_output,
            links={
                "self": f"/api/tasks/{task.id}",
                "update": f"/api/tasks/{task.id}/update",
                "delete": f"/api/tasks/{task.id}/delete",
                "list": "/api/tasks"
            }
        )