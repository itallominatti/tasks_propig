from uuid import UUID

from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository
from src.core.user.application.use_cases.list_users import ListUsers
from src.core.user.application.use_cases.create_user import CreateUser
from src.adapters.hash.bcrypt_adapter import BcryptPasswordHasher


class TestListUsers:
    def test_list_user_with_valid_data(self):
        repository = InMemoryUserRepository()
        hasher = BcryptPasswordHasher()

        use_case = CreateUser(repository=repository, password_hasher=hasher)
        request = CreateUser.CreateUserRequest(
            username="John Doe", email="jhondoe@gmail.com", password="securepassword123"
        )

        response = use_case.execute(request)

        assert response.id is not None
        assert isinstance(response, CreateUser.CreateUserResponse)
        assert isinstance(response.id, UUID)

        use_case_get = ListUsers(repository=repository)
        request_get = ListUsers.ListUsersRequest(
            order_by="username",
            current_page=1,
            page_size=10
        )
        response_get = use_case_get.execute(request_get)
        assert len(response_get.data) == 1
        assert response_get.data[0].username == "John Doe"
        assert response_get.data[0].email == "jhondoe@gmail.com"
        assert response_get.data[0].links["self"] == f"/api/users/{response.id}"
        assert response_get.meta.total_users == 1
        assert response_get.meta.current_page == 1
        assert response_get.meta.page_size == 10
        assert response_get.meta.query_params == {
            "order_by": "username",
            "page": 1,
            "size": 10
        }

    
