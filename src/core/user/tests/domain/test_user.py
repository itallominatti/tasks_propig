import uuid
from uuid import UUID

import pytest

from src.core.user.domain.user import User

class TestUser:
    def test_create_user_when_the_name_is_empty(self):
        with pytest.raises(
            ValueError, match="username_required: Username is required."
            ) as exc_info:
            User(username="", email="teste@gmail.com", password="12345678")
        assert "username_required: Username is required." in str(exc_info.value)

    def test_create_user_when_the_email_is_empty(self):
        with pytest.raises(
            ValueError, match="email_required: Email is required."
            ) as exc_info:
            User(username="test", email="", password="12345678")
        assert "email_required: Email is required." in str(exc_info.value)

    def test_create_user_when_the_email_is_invalid(self):
        with pytest.raises(
            ValueError, match="email_invalid: Email is invalid."
            ) as exc_info:
            User(username="test", email="invalid-email", password="12345678")
        assert "email_invalid: Email is invalid." in str(exc_info.value)

    def test_create_user_when_the_password_is_empty(self):
        with pytest.raises(
            ValueError, match="password_required: Password is required."
            ) as exc_info:
            User(username="test", email="teste@gmail.com", password="")
        assert "password_required: Password is required." in str(exc_info.value)

    def test_create_user_when_is_active_is_not_a_boolean(self):
        with pytest.raises(
            ValueError, match="is_active_invalid: is_active must be a boolean value."
            ) as exc_info:
            User(username="test", email="teste@gmail.com", password="12345678", is_active="yes")
        assert "is_active_invalid: is_active must be a boolean value." in str(exc_info.value)

    def test_create_user_with_valid_data(self):
        user = User(username="test", email="teste@gmail.com", password="Senha123")
        assert isinstance(user, User)