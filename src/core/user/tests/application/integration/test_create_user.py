from uuid import UUID

from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository
from src.core.user.application.use_cases.create_user import CreateUser
from src.adapters.hash.bcrypt_adapter import BcryptPasswordHasher

class TestCreateUser:
    def test_create_user_with_valid_data(self):
        repository = InMemoryUserRepository()
        hasher = BcryptPasswordHasher()

        use_case = CreateUser(
            repository=repository,
            password_hasher=hasher
        )
        request = CreateUser.CreateUserRequest(
            username="John Doe",
            email="jhondoe@gmail.com",
            password="securepassword123"
        )

        response = use_case.execute(request)

        assert response.id is not None
        assert isinstance(response, CreateUser.CreateUserResponse)
        assert isinstance(response.id, UUID)
