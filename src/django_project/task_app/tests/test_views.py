import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from src.django_project.user_app.models import User as DjangoUserModel
from src.django_project.task_app.models import Task as DjangoTaskModel

@pytest.mark.django_db
class TestTaskAPIFlow(APITestCase):
    def test_create_user_login_and_create_task(self):
        # Cria usuário
        user_data = {
            "username": "teste",
            "password": "securepassword123",
            "email": "teste@gmail.com"
        }
        create_response = self.client.post(
            '/api/users/',
            user_data,
            format='json'
        )
        assert create_response.status_code == status.HTTP_201_CREATED

        login_response = self.client.post(
            '/auth/login/',
            {
                "username": "teste",
                "password": "securepassword123"
            },
            format='json'
        )
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        task_response = self.client.post(
            '/api/tasks/',
            {
                "title": "teste para testar description",
                "description": "teste description"
            },
            format='json'
        )
        assert task_response.status_code == status.HTTP_201_CREATED
        data = task_response.data
        assert "id" in data
        assert data["id"] is not None

        task = DjangoTaskModel.objects.get(id=data["id"])
        assert task.title == "teste para testar description"
        assert task.description == "teste description"
        user = DjangoUserModel.objects.get(username="teste")
        assert user in task.users.all()

    def test_create_task_without_authentication(self):
        task_response = self.client.post(
            '/api/tasks/',
            {
                "title": "teste para testar description",
                "description": "teste description"
            },
            format='json'
        )
        assert task_response.status_code == status.HTTP_403_FORBIDDEN
        assert task_response.data['detail'] == 'Authentication credentials were not provided.'

    def test_create_task_with_invalid_data(self):
        user_data = {
            "username": "teste",
            "password": "securepassword123",
            "email": "teste@gmail.com"
        }
        create_response = self.client.post(
            '/api/users/',
            user_data,
            format='json'
        )
        assert create_response.status_code == status.HTTP_201_CREATED

        login_response = self.client.post(
            '/auth/login/',
            {
                "username": "teste",
                "password": "securepassword123"
            },
            format='json'
        )
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        task_response = self.client.post(
            '/api/tasks/',
            {
                "title": "",  # Invalid title
                "description": "teste description"
            },
            format='json'
        )
        assert task_response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestTaskAPIFlow(APITestCase):
    # ...outros testes...

    def test_list_tasks_authenticated(self):
        # Cria usuário e autentica
        user_data = {
            "username": "teste",
            "password": "securepassword123",
            "email": "teste@gmail.com"
        }
        create_response = self.client.post(
            '/api/users/',
            user_data,
            format='json'
        )
        assert create_response.status_code == status.HTTP_201_CREATED

        login_response = self.client.post(
            '/auth/login/',
            {
                "username": "teste",
                "password": "securepassword123"
            },
            format='json'
        )
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Cria algumas tasks
        for i in range(3):
            task_response = self.client.post(
                '/api/tasks/',
                {
                    "title": f"Task {i}",
                    "description": f"Description {i}"
                },
                format='json'
            )
            assert task_response.status_code == status.HTTP_201_CREATED

        # Lista tasks
        list_response = self.client.get('/api/tasks/?order_by=title&page=1&size=10')
        assert list_response.status_code == status.HTTP_200_OK
        data = list_response.data
        assert "data" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) >= 3  # Deve ter pelo menos as 3 criadas
        assert "meta" in data
        assert "links" in data

    def test_list_tasks_unauthenticated(self):
        response = self.client.get('/api/tasks/')
        assert response.status_code == status.HTTP_403_FORBIDDEN or response.status_code == status.HTTP_401_UNAUTHORIZED