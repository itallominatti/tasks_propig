from uuid import UUID
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

from src.core.tasks.domain.task_repository_interface import TaskRepositoryInterface
from src.core.tasks.application.exceptions import InvalidTaskBy

@dataclass
class TaskOutput:
    id: UUID
    title: str
    description: str
    status: str
    created_at: str
    updated_at: str
    users: set[UUID]
    links: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MetaOutput:
    total_tasks: int
    current_page: int
    page_size: int
    query_params: dict[str, Any] = field(default_factory=dict)

class ListTask:
    def __init__(self, repository: TaskRepositoryInterface) -> None:
        self.repository = repository

    @dataclass
    class ListTaskRequest:
        order_by: str = "title"
        page: int = 1
        size: int = 10
        user_id: UUID = None

    @dataclass
    class ListTaskResponse:
        data: List[TaskOutput]
        meta: MetaOutput = field(default_factory=lambda: MetaOutput(0, 1, 10, {}))
        links: Dict[str, Any] = field(default_factory=dict)

    def execute(self, request: ListTaskRequest) -> ListTaskResponse:
        if not request.user_id:
            raise ValueError("User ID must be provided in the request.")

        tasks = self.repository.list(
            user_id=request.user_id
        )

        if request.order_by not in ['title', 'status', 'created_at', 'updated_at']:
            raise InvalidTaskBy(f"Invalid order_by field: {request.order_by}")

        sorted_tasks = sorted(
            [task for task in tasks if hasattr(task, request.order_by)],
            key=lambda x: getattr(x, request.order_by)
        )
        page_offset = (request.page - 1) * request.size
        paginated_tasks = sorted_tasks[page_offset:page_offset + request.size]

        task_outputs = [
            TaskOutput(
                id=task.id,
                title=task.title,
                description=task.description,
                status=task.status,
                created_at=task.created_at.isoformat(),
                updated_at=task.updated_at.isoformat(),
                users=set(task.users),
                links={
                    "self": f"/api/tasks/{task.id}",
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
                    "get": {
                        "method": "GET",
                        "href": f"/api/tasks/{task.id}",
                        "description": "Get task details."
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
            for task in paginated_tasks
        ]

        return self.ListTaskResponse(
            data=task_outputs,
            meta=MetaOutput(
                total_tasks=len(sorted_tasks),
                current_page=request.page,
                page_size=request.size,
                query_params={
                    "order_by": request.order_by,
                    "page": request.page,
                    "size": request.size
                }
            ),
            links={
                "list": {
                    "method": "GET",
                    "href": "/api/tasks",
                    "description": "List all tasks with pagination and sorting options."
                },
                "self": f"/api/tasks?page={request.page}&size={request.size}&order_by={request.order_by}",
                "next": f"/api/tasks?page={request.page + 1}&size={request.size}&order_by={request.order_by}" if len(sorted_tasks) > page_offset + request.size else None,
                "prev": f"/api/tasks?page={request.page - 1}&size={request.size}&order_by={request.order_by}" if request.page > 1 else None,
                "first": f"/api/tasks?page=1&size={request.size}&order_by={request.order_by}",
                "last": f"/api/tasks?page={((len(sorted_tasks) - 1) // request.size) + 1}&size={request.size}&order_by={request.order_by}",
            }
        )