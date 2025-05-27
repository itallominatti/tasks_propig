from uuid import UUID
import pytest

from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository
from src.core.user.application.use_cases.create_user import CreateUser
from src.adapters.hash.bcrypt_adapter import BcryptPasswordHasher
from src.core.user.application.exceptions import UserAlreadyExists, InvalidUser

class TestCreateUser:
    def test_create_user_with_valid_data(self):
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

    def test_create_user_with_existing_email(self):
        repository = InMemoryUserRepository()
        hasher = BcryptPasswordHasher()
        use_case = CreateUser(repository=repository, password_hasher=hasher)

        request1 = CreateUser.CreateUserRequest(
            username="John Doe", email="jhondoe@gmail.com", password="securepassword123"
        )
        use_case.execute(request1)

        
        request2 = CreateUser.CreateUserRequest(
            username="Jane Doe", email="jhondoe@gmail.com", password="anotherpassword123"
        )
        with pytest.raises(UserAlreadyExists):
            use_case.execute(request2)

    def test_create_user_with_invalid_password(self):
        repository = InMemoryUserRepository()
        hasher = BcryptPasswordHasher()
        use_case = CreateUser(repository=repository, password_hasher=hasher)

        request = CreateUser.CreateUserRequest(
            username="John Doe", email="jhondoe2@gmail.com", password="short"
        )
        with pytest.raises(InvalidUser):
            use_case.execute(request)