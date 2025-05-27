from uuid import UUID

from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository
from src.core.user.application.use_cases.get_user import GetUser
from src.core.user.application.use_cases.create_user import CreateUser
from src.adapters.hash.bcrypt_adapter import BcryptPasswordHasher


class TestGetUser:
    def test_get_user_with_valid_data(self):
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

        use_case_get = GetUser(repository=repository)
        request_get = GetUser.GetUserRequest(id=response.id)
        response_get = use_case_get.execute(request_get)

        assert response_get.username == "John Doe"
        assert response_get.email == "jhondoe@gmail.com"
        assert response_get.is_active is True
        assert "self" in response_get.links
        assert response_get.links["self"] == f"/api/users/{response.id}"
        assert "list" in response_get.links
        assert response_get.links["list"]["method"] == "GET"
        assert response_get.links["list"]["href"] == "/api/users"
        assert "create" in response_get.links
        assert response_get.links["create"]["method"] == "POST"
        assert response_get.links["create"]["href"] == "/api/users"
        assert response_get.links["create"]["body"] == {
            "email": "string",
            "username": "string",
            "password": "string",
            "is_active": "boolean (optional, default is True)"
        }


    
