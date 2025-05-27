import uuid
from unittest.mock import create_autospec

import pytest

from src.core.user.application.use_cases.get_user import GetUser

from src.core.user.domain.user_repository_interface import UserRepositoryInterface
from src.core.user.domain.user import User
from src.core.user.application.exceptions import UserNotFound

class TestGetUser:
    def test_return_found_user(self):

        user = User(
            id=uuid.uuid4(),
            email="teste@gmail.com",
            username="teste",
            password="securepassword123",
        )
        mock_repository = create_autospec(UserRepositoryInterface)
        mock_repository.get_user_by_id.return_value = user

        use_case = GetUser(repository=mock_repository)
        response = use_case.execute(request=GetUser.GetUserRequest(id=user.id))

        assert isinstance(response, GetUser.GetUserResponse)
        assert response.username == user.username

    def test_raise_user_not_found(self):
        mock_repository = create_autospec(UserRepositoryInterface)
        mock_repository.get_user_by_id.return_value = None

        use_case = GetUser(repository=mock_repository)

        with pytest.raises(UserNotFound):
            use_case.execute(request=GetUser.GetUserRequest(id=uuid.uuid4()))



