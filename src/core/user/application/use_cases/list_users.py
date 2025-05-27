from dataclasses import dataclass, field
from uuid import UUID
from typing import List, Dict, Any

from src.core.user.domain.user_repository_interface import UserRepositoryInterface
from src.core.user.application.exceptions import InvalidOrderBy

@dataclass
class UserOutput:
    id: UUID
    username: str
    email: str
    links: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MetaOutput:
    total_users: int
    current_page: int
    page_size: int
    query_params: dict[str]

class ListUsers:
    @dataclass
    class ListUsersRequest:
        order_by: str = "username"
        current_page: int = 1
        page_size: int = 10

    @dataclass
    class ListUsersResponse:
        data: list[UserOutput]
        meta: MetaOutput = field(default_factory=lambda: MetaOutput(0, 1, 10, {}))
        links: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, repository: UserRepositoryInterface) -> None:
        self.repository = repository

    def execute(self, request: ListUsersRequest) -> ListUsersResponse:
        users = self.repository.list()

        if request.order_by not in ['username', 'email', 'id']:
            raise InvalidOrderBy(f"Invalid order_by field: {request.order_by}")

        sorted_users = sorted(
            [user for user in users if hasattr(user, request.order_by)],
            key=lambda x: getattr(x, request.order_by)
        )
        page_offset = (request.current_page - 1) * request.page_size
        paginated_users = sorted_users[page_offset:page_offset + request.page_size]

        user_outputs = [
            UserOutput(
                id=user.id,
                username=user.username,
                email=user.email,
                links={
                    "self": f"/api/users/{user.id}",
                }
            )
            for user in paginated_users
        ]

        return self.ListUsersResponse(
            data=user_outputs,
            meta=MetaOutput(
                total_users=len(sorted_users),
                current_page=request.current_page,
                page_size=request.page_size,
                query_params={
                    "order_by": request.order_by,
                    "page": request.current_page,
                    "size": request.page_size
                }
            ),
            links={
                "self": f"/api/users?page={request.current_page}&size={request.page_size}&order_by={request.order_by}",
                "next": f"/api/users?page={request.current_page + 1}&size={request.page_size}&order_by={request.order_by}" if len(sorted_users) > page_offset + request.page_size else None,
                "prev": f"/api/users?page={max(1, request.current_page - 1)}&size={request.page_size}&order_by={request.order_by}" if request.current_page > 1 else None,
                "first": f"/api/users?page=1&size={request.page_size}&order_by={request.order_by}",
                "last": f"/api/users?page={((len(sorted_users) - 1) // request.page_size) + 1}&size={request.page_size}&order_by={request.order_by}",
                "create": {
                    "method": "POST",
                    "href": "/api/users",
                    "description": "Create a new user with params: username, email, password and is_active (optional)"
                }
            }
        )