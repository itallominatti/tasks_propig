from uuid import UUID
from dataclasses import dataclass, field
from typing import Any

from src.core.user.application.exceptions import UserNotFound
from src.core.user.domain.user_repository_interface import UserRepositoryInterface

class GetUser:
    @dataclass
    class GetUserRequest:
        id: UUID

    @dataclass
    class GetUserResponse:
        username: str
        email: str
        is_active: bool
        links: dict[str, Any] = field(default_factory=dict)

    def __init__(self, repository: UserRepositoryInterface) -> None:
        self.repository = repository

    def execute(self, request: "GetUser.GetUserRequest") -> "GetUser.GetUserResponse":
        user = self.repository.get_user_by_id(request.id)
        if user is None:
            raise UserNotFound(f"User with id {request.id} not found.")
        
        return self.GetUserResponse(
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            links={
                "self": f"/api/users/{user.id}",
                "list": {
                    "method": "GET",
                    "href": "/api/users",
                    "query_params": {
                        "order_by": "username or email",
                        "page": 1,
                        "size": 10
                    },
                    "description": "List all users with pagination and sorting options."
                },
                "create": {
                    "method": "POST",
                    "href": "/api/users",
                    "description": "Create a new user.",
                    "body": {
                        "email": "string",
                        "username": "string",
                        "password": "string",
                        "is_active": "boolean (optional, default is True)"
                    }
                }
            }
        )