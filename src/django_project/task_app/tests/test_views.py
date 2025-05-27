import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from src.django_project.user_app.models import User as DjangoUserModel
from src.django_project.task_app.models import Task as DjangoTaskModel

from src.core.user.domain.user import User

@pytest.mark.django_db
class TestTaskEndpoint(APITestCase):

    def setUp(self):
        user_data = {
            "username": "testuser",
            "email": "testeuser@gmail.com",
            "password": "securepassword123"
        }
        create_response = self.client.post(
            '/api/users/',
            user_data,
            format='json'
        )
        assert create_response.status_code == status.HTTP_201_CREATED

        # Pegue o usuário real do banco Django
        self.user = DjangoUserModel.objects.get(username="testuser")

        login_response = self.client.post(
            '/auth/login/',
            {
                "username": "testuser",
                "password": "securepassword123"
            },
            format='json'
        )
        assert login_response.status_code == status.HTTP_200_OK
        self.token = login_response.data['token']

    def test_create_task_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(
            '/api/tasks/',
            {
                "title": "Minha Task",
                "description": "Descrição da task",
                "users": [str(self.user.id)]
            },
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        assert "id" in data
        task = DjangoTaskModel.objects.get(id=data["id"])
        user_ids = set(str(u.id) for u in task.users.all())
        assert str(self.user.id) in user_ids

    def test_create_task_unauthenticated(self):
        response = self.client.post(
            '/api/tasks/',
            {
                "title": "Task sem auth",
                "description": "Descrição",
                "users": [str(self.user.id)]
            },
            format='json'
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_task_user_not_in_users(self):
        """
        Se o usuário autenticado não estiver na lista de users enviada, 
        a API deve forçar a inclusão dele (ou rejeitar, dependendo da regra).
        Aqui testamos que a task criada sempre inclui o user autenticado.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        # Envia uma lista vazia, mas a view deve incluir o user autenticado
        response = self.client.post(
            '/api/tasks/',
            {
                "title": "Task com users vazio",
                "description": "Descrição",
                "users": []
            },
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.data
        task = DjangoTaskModel.objects.get(id=data["id"])
        user_ids = set(str(u.id) for u in task.users.all())
        assert str(self.user.id) in user_ids