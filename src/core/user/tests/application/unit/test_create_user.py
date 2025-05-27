from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.core.user.application.use_cases.create_user import CreateUser
from src.core.user.application.exceptions import InvalidUser
from src.core.user.domain.user_repository_interface import UserRepositoryInterface
from src.adapters.hash.hash_adapter_interface import PasswordHasherInterface

class TestCreateUser:
    def test_create_user_with_valid_data(self):
        mock_repository = MagicMock(UserRepositoryInterface)
        mock_repository.get_by_email.return_value = None  # Ajuste aqui
        mock_password_hasher = MagicMock(spec=PasswordHasherInterface)
        mock_password_hasher.hash.return_value = "hashed_password"
        use_case = CreateUser(
            repository=mock_repository,
            password_hasher=mock_password_hasher
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
        assert mock_repository.save.called is True

    def test_create_user_with_invalid_email(self):
        mock_repository = MagicMock(UserRepositoryInterface)
        mock_repository.get_by_email.return_value = None
        mock_password_hasher = MagicMock(spec=PasswordHasherInterface)
        mock_password_hasher.hash.return_value = "hashed_password"
        use_case = CreateUser(
            repository=mock_repository,
            password_hasher=mock_password_hasher
        )
        request = CreateUser.CreateUserRequest(
            username="John Doe",
            email="invalid-email",
            password="securepassword123"
        )

        with pytest.raises(InvalidUser) as exc_info:
            use_case.execute(request)

        assert "Email is invalid." in str(exc_info.value)
        assert not mock_repository.save.called

    def test_create_user_with_invalid_password(self):
        mock_repository = MagicMock(UserRepositoryInterface)
        mock_repository.get_by_email.return_value = None
        mock_password_hasher = MagicMock(spec=PasswordHasherInterface)
        mock_password_hasher.hash.return_value = "hashed_password"
        use_case = CreateUser(
            repository=mock_repository,
            password_hasher=mock_password_hasher
        )
        request = CreateUser.CreateUserRequest(
            username="John Doe",
            email="jhondoe@gmail.com",
            password="short"
        )
        with pytest.raises(InvalidUser) as exc_info:
            use_case.execute(request)
        assert "Password must be at least 8 characters long and contain both letters and numbers." in str(exc_info.value)
        assert not mock_repository.save.called

    def test_create_user_with_empty_username(self):
        mock_repository = MagicMock(UserRepositoryInterface)
        mock_repository.get_by_email.return_value = None
        mock_password_hasher = MagicMock(spec=PasswordHasherInterface)
        mock_password_hasher.hash.return_value = "hashed_password"
        use_case = CreateUser(
            repository=mock_repository,
            password_hasher=mock_password_hasher
        )
        request = CreateUser.CreateUserRequest(
            username="",
            email="jhondoe@gmail.com",
            password="securepassword123"
        )
        with pytest.raises(InvalidUser) as exc_info:
            use_case.execute(request)

        assert "Username is required." in str(exc_info.value)
        assert not mock_repository.save.called

    def test_create_user_with_empty_email(self):
        mock_repository = MagicMock(UserRepositoryInterface)
        mock_repository.get_by_email.return_value = None
        mock_password_hasher = MagicMock(spec=PasswordHasherInterface)
        mock_password_hasher.hash.return_value = "hashed_password"
        use_case = CreateUser(
            repository=mock_repository,
            password_hasher=mock_password_hasher
        )
        request = CreateUser.CreateUserRequest(
            username="John Doe",
            email="",
            password="securepassword123"
        )
        with pytest.raises(InvalidUser) as exc_info:
            use_case.execute(request)

        assert "Email is required." in str(exc_info.value)
        assert not mock_repository.save.called

    def test_create_user_with_invalid_is_active(self):
        mock_repository = MagicMock(UserRepositoryInterface)
        mock_repository.get_by_email.return_value = None
        mock_password_hasher = MagicMock(spec=PasswordHasherInterface)
        mock_password_hasher.hash.return_value = "hashed_password"
        use_case = CreateUser(
            repository=mock_repository,
            password_hasher=mock_password_hasher
        )
        request = CreateUser.CreateUserRequest(
            username="John Doe",
            email="jhondoe@gmail.com",
            password="securepassword123",
            is_active="not_a_boolean"
        )
        with pytest.raises(InvalidUser) as exc_info:
            use_case.execute(request)
        assert "is_active must be a boolean value." in str(exc_info.value)
        assert not mock_repository.save.called

    def test_create_user_with_valid_is_active(self):
        mock_repository = MagicMock(UserRepositoryInterface)
        mock_repository.get_by_email.return_value = None
        mock_password_hasher = MagicMock(spec=PasswordHasherInterface)
        mock_password_hasher.hash.return_value = "hashed_password"
        use_case = CreateUser(
            repository=mock_repository,
            password_hasher=mock_password_hasher
        )
        request = CreateUser.CreateUserRequest(
            username="John Doe",
            email="jhondoe@gmail.com",
            password="securepassword123",
            is_active=True
        )
        response = use_case.execute(request)
        assert response.id is not None
        assert isinstance(response, CreateUser.CreateUserResponse)
        assert isinstance(response.id, UUID)
        assert mock_repository.save.called is True