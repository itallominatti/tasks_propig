from uuid import UUID
from dataclasses import dataclass, field

from src.core.tasks.application.exceptions import RelatedUserNotFound, InvalidTaskData
from src.core.tasks.domain.tasks import Task

class CreateTask:
    def __init__(self, repository, user_repository):
        self.repository = repository
        self.user_repository = user_repository

    @dataclass
    class CreateTaskRequest:
        title: str
        description: str = ""
        user_ids: set[UUID] = field(default_factory=set)

    @dataclass
    class CreateTaskResponse:
        id: UUID
        links: dict = field(default_factory=dict)

    def execute(self, request: CreateTaskRequest) -> 'CreateTask.CreateTaskResponse':
        user_ids = {user.id for user in self.user_repository.list()}

        if not request.user_ids.issubset(user_ids):
            raise RelatedUserNotFound("One or more users do not exist in the system.")

        try:
            task = Task(
                title=request.title,
                description=request.description,
                users=request.user_ids
            )
        except ValueError as err:
            raise InvalidTaskData(f"Invalid task data: {err}")

        self.repository.save(task)
        return self.CreateTaskResponse(
            id=task.id,
            links={
                "list": {
                    "method": "GET",
                    "href": "/api/tasks",
                    "query_params": {
                        "order_by": "title or created_at",
                        "page": 1,
                        "size": 10
                    },
                    "description": "List all tasks with pagination and sorting options."
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