import pytest
from unittest.mock import MagicMock

from src.core.user.application.use_cases.authenticate_user import AuthenticateUser
from src.core.user.application.exceptions import InvalidUser

class DummyUser:
    def __init__(self, id):
        self.id = id

    def check_password(self, password, hash_adapter):
        return password == "valid_password"

def test_authenticate_user_success():
    mock_repository = MagicMock()
    mock_jwt_adapter = MagicMock()
    dummy_user = DummyUser(id=123)
    mock_repository.get_user_by_username.return_value = dummy_user
    mock_jwt_adapter.encode.return_value = "jwt_token"

    use_case = AuthenticateUser(
        repository=mock_repository,
        jwt_adapter=mock_jwt_adapter,
        token_exp_minutes=60
    )

    request = AuthenticateUser.AuthenticateUserRequest(
        username="john",
        password="valid_password"
    )

    response = use_case.execute(request)

    assert response.token == "jwt_token"
    assert response.expires_at is not None
    mock_repository.get_user_by_username.assert_called_once_with("john")
    mock_jwt_adapter.encode.assert_called_once()

def test_authenticate_user_invalid_password():
    mock_repository = MagicMock()
    mock_jwt_adapter = MagicMock()
    dummy_user = DummyUser(id=123)
    dummy_user.check_password = lambda password, hash_adapter: False
    mock_repository.get_user_by_username.return_value = dummy_user

    use_case = AuthenticateUser(
        repository=mock_repository,
        jwt_adapter=mock_jwt_adapter,
        token_exp_minutes=60
    )

    request = AuthenticateUser.AuthenticateUserRequest(
        username="john",
        password="wrong_password"
    )

    with pytest.raises(InvalidUser):
        use_case.execute(request)

def test_authenticate_user_user_not_found():
    mock_repository = MagicMock()
    mock_jwt_adapter = MagicMock()
    mock_repository.get_user_by_username.return_value = None

    use_case = AuthenticateUser(
        repository=mock_repository,
        jwt_adapter=mock_jwt_adapter,
        token_exp_minutes=60
    )

    request = AuthenticateUser.AuthenticateUserRequest(
        username="notfound",
        password="any"
    )

    with pytest.raises(InvalidUser):
        use_case.execute(request)