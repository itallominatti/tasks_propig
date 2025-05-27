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


@pytest.mark.django_db
class TestAPITaskRetrieve(APITestCase):
    def test_retrieve_task_authenticated(self):
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

        # Cria uma task
        task_response = self.client.post(
            '/api/tasks/',
            {
                "title": "Retrieve Task",
                "description": "Retrieve description"
            },
            format='json'
        )
        assert task_response.status_code == status.HTTP_201_CREATED
        task_id = task_response.data["id"]

        # Recupera a task
        retrieve_response = self.client.get(f'/api/tasks/{task_id}/')
        assert retrieve_response.status_code == status.HTTP_200_OK
        data = retrieve_response.data
        assert data["id"] == task_id
        assert data["title"] == "Retrieve Task"
        assert data["description"] == "Retrieve description"
        assert "links" in data

    def test_retrieve_task_not_found(self):
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

        # Tenta recuperar uma task inexistente
        import uuid
        fake_id = str(uuid.uuid4())
        retrieve_response = self.client.get(f'/api/tasks/{fake_id}/')
        assert retrieve_response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestAPITaskUpdate(APITestCase):
    def setUp(self):
        user_data = {
            "username": "teste",
            "password": "securepassword123",
            "email": "teste@gmail.com"
        }
        create_response = self.client.post('/api/users/', user_data, format='json')
        assert create_response.status_code == status.HTTP_201_CREATED

        login_response = self.client.post(
            '/auth/login/',
            {"username": "teste", "password": "securepassword123"},
            format='json'
        )
        assert login_response.status_code == status.HTTP_200_OK
        self.token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Cria uma task para os testes
        task_response = self.client.post(
            '/api/tasks/',
            {"title": "Task to Update", "description": "Initial description"},
            format='json'
        )
        assert task_response.status_code == status.HTTP_201_CREATED
        self.task_id = task_response.data["id"]

    def test_update_task_authenticated(self):
        update_response = self.client.put(
            f'/api/tasks/{self.task_id}/',
            {
                "title": "Updated Title",
                "description": "Updated description",
                "status": "completed"
            },
            format='json'
        )
        assert update_response.status_code == status.HTTP_204_NO_CONTENT

        # Verifica se os dados foram realmente atualizados
        get_response = self.client.get(f'/api/tasks/{self.task_id}/')
        assert get_response.status_code == status.HTTP_200_OK
        data = get_response.data
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated description"
        assert data["status"] == "completed"

    def test_partial_update_task_authenticated(self):
        patch_response = self.client.patch(
            f'/api/tasks/{self.task_id}/',
            {
                "description": "Patched description"
            },
            format='json'
        )
        assert patch_response.status_code == status.HTTP_204_NO_CONTENT

        # Verifica se só o campo alterado foi atualizado
        get_response = self.client.get(f'/api/tasks/{self.task_id}/')
        assert get_response.status_code == status.HTTP_200_OK
        data = get_response.data
        assert data["description"] == "Patched description"
        assert data["title"] == "Task to Update"  # O título permanece igual

    def test_update_task_not_found(self):
        import uuid
        fake_id = str(uuid.uuid4())
        update_response = self.client.put(
            f'/api/tasks/{fake_id}/',
            {
                "title": "Should Not Exist",
                "description": "Should Not Exist",
                "status": "completed"
            },
            format='json'
        )
        assert update_response.status_code == status.HTTP_404_NOT_FOUND

    def test_partial_update_task_not_found(self):
        import uuid
        fake_id = str(uuid.uuid4())
        patch_response = self.client.patch(
            f'/api/tasks/{fake_id}/',
            {
                "description": "Should Not Exist"
            },
            format='json'
        )
        assert patch_response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestTaskAPIDelete(APITestCase):
    def setUp(self):
        user_data = {
            "username": "teste",
            "password": "securepassword123",
            "email": "teste@gmail.com"
        }
        create_response = self.client.post('/api/users/', user_data, format='json')
        assert create_response.status_code == status.HTTP_201_CREATED

        login_response = self.client.post(
            '/auth/login/',
            {"username": "teste", "password": "securepassword123"},
            format='json'
        )
        assert login_response.status_code == status.HTTP_200_OK
        self.token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Cria uma task para os testes
        task_response = self.client.post(
            '/api/tasks/',
            {"title": "Task to Delete", "description": "Initial description"},
            format='json'
        )
        assert task_response.status_code == status.HTTP_201_CREATED
        self.task_id = task_response.data["id"]

    def test_delete_task_authenticated(self):
        delete_response = self.client.delete(f'/api/tasks/{self.task_id}/')
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        # Verifica se foi realmente deletada
        get_response = self.client.get(f'/api/tasks/{self.task_id}/')
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_task_not_found(self):
        import uuid
        fake_id = str(uuid.uuid4())
        delete_response = self.client.delete(f'/api/tasks/{fake_id}/')
        assert delete_response.status_code == status.HTTP_404_NOT_FOUND