import uuid

import pytest

from rest_framework import status
from rest_framework.test import APITestCase

from src.core.user.domain.user import User

@pytest.mark.django_db
class TestUserEndpoint(APITestCase):
    def test_when_id_is_invalid_return_400(self):
        """Test that an invalid UUID returns a 400 Bad Request."""
        invalid_id = "invalid-uuid"
        user = User(
            id=invalid_id,
            username="testuser",
            email="test@gmail.com",
            password="securepassword123"
            )
        response = self.client.post(
            "/api/users/",
            data={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "password": user.password
            },
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST