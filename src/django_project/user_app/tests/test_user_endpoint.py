import pytest

from rest_framework import status
from rest_framework.test import APITestCase

from src.django_project.user_app.models import User as DjangoUserModel

@pytest.mark.django_db
class TestUserEndpoint(APITestCase):

    def test_list_users(self):

        self.client.post(
            '/api/users/',
            {
                "username": "testuser",
                "email": "teste@gmail.com",
                "password": "securepassword123"
            },
        )

        login_response = self.client.post(
            '/auth/login/',
            {
                "username": "testuser",
                "password": "securepassword123"
            },
            format='json'
        )
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/users/')

        assert response.status_code == status.HTTP_200_OK
        data = response.data
        if isinstance(data, dict) and "data" in data:
            data = data["data"]
        assert len(data) == 1

        user = DjangoUserModel.objects.get(username="testuser")
        assert data[0]['username'] == user.username
        assert data[0]['email'] == user.email

    def test_create_user(self):
        response = self.client.post(
            '/api/users/',
            {
                "username": "newuser",
                "email": "newuser@gmail.com",
                "password": "newsecurepassword123"
            },
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_user_with_existing_username(self):
        self.client.post(
            '/api/users/',
            {
                "username": "existinguser",
                "email": "existinguser",
                "password": "existingpassword123"
            },
            format='json'
        )
        response = self.client.post(
            '/api/users/',
            {
                "username": "existinguser",
                "email": "existinguser",
                "password": "newpassword123"
            },
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_user_with_existing_email(self):
        self.client.post(
            '/api/users/',
            {
                "username": "user1",
                "email": "user1@gmail.com",
                "password": "password123",
            },
            format='json'
        )
        response = self.client.post(
            '/api/users/',
            {
                "username": "user2",
                "email": "user1@gmail.com",
                "password": "password456",
            },
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST