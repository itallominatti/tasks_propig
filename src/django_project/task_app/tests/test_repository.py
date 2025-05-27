import uuid
import pytest
from django.db import transaction

from src.core.tasks.domain.tasks import Task
from src.django_project.task_app.repository import DjangoOrmTaskRepository
from src.django_project.task_app.models import Task as DjangoTaskModel
from src.django_project.user_app.models import User as DjangoUserModel

@pytest.mark.django_db
class TestSave:
    def test_saves_task_in_database(self):
        user = DjangoUserModel.objects.create(
            id=uuid.uuid4(),
            username="user1",
            email="user1@email.com",
            password="securepassword123"
        )
        task = Task(
            title="My Task",
            description="A test task",
            users={user.id}
        )
        repo = DjangoOrmTaskRepository()
        assert DjangoTaskModel.objects.count() == 0
        repo.save(task)
        assert DjangoTaskModel.objects.count() == 1
        task_model = DjangoTaskModel.objects.first()
        assert task_model.id == task.id
        assert task_model.title == "My Task"
        assert task_model.description == "A test task"
        assert user in task_model.users.all()

@pytest.mark.django_db
class TestGetById:
    def test_get_by_id_when_task_exists(self):
        user = DjangoUserModel.objects.create(
            id=uuid.uuid4(),
            username="user2",
            email="user2@email.com",
            password="securepassword123"
        )
        task = Task(
            title="Task 2",
            description="Another test task",
            users={user.id}
        )
        repo = DjangoOrmTaskRepository()
        repo.save(task)
        found = repo.get_by_id(task.id)
        assert found is not None
        assert found.id == task.id
        assert user.id in found.users

    def test_get_by_id_when_task_not_found(self):
        repo = DjangoOrmTaskRepository()
        assert repo.get_by_id(uuid.uuid4()) is None

@pytest.mark.django_db
class TestDelete:
    def test_delete_task(self):
        user = DjangoUserModel.objects.create(
            id=uuid.uuid4(),
            username="user3",
            email="user3@email.com",
            password="securepassword123"
        )
        task = Task(
            title="Task 3",
            description="Task to delete",
            users={user.id}
        )
        repo = DjangoOrmTaskRepository()
        repo.save(task)
        assert DjangoTaskModel.objects.count() == 1
        repo.delete(task.id)
        assert DjangoTaskModel.objects.count() == 0

@pytest.mark.django_db
class TestUpdate:
    def test_update_task_title(self):
        user = DjangoUserModel.objects.create(
            id=uuid.uuid4(),
            username="user4",
            email="user4@email.com",
            password="securepassword123"
        )
        task = Task(
            title="Old Title",
            description="Task to update",
            users={user.id}
        )
        repo = DjangoOrmTaskRepository()
        repo.save(task)
        task.title = "New Title"
        repo.update(task)
        updated = DjangoTaskModel.objects.get(id=task.id)
        assert updated.title == "New Title"

    def test_update_task_users(self):
        user1 = DjangoUserModel.objects.create(
            id=uuid.uuid4(),
            username="user5",
            email="user5@email.com",
            password="securepassword123"
        )
        user2 = DjangoUserModel.objects.create(
            id=uuid.uuid4(),
            username="user6",
            email="user6@email.com",
            password="securepassword123"
        )
        task = Task(
            title="Task with users",
            description="Testing users update",
            users={user1.id}
        )
        repo = DjangoOrmTaskRepository()
        repo.save(task)
        task.users.add(user2.id)
        repo.update(task)
        updated = DjangoTaskModel.objects.get(id=task.id)
        user_ids = {u.id for u in updated.users.all()}
        assert user1.id in user_ids
        assert user2.id in user_ids

@pytest.mark.django_db
class TestList:
    def test_list_tasks(self):
        user = DjangoUserModel.objects.create(
            id=uuid.uuid4(),
            username="user7",
            email="user7@email.com",
            password="securepassword123"
        )
        repo = DjangoOrmTaskRepository()
        task1 = Task(
            title="Task 1",
            description="First task",
            users={user.id}
        )
        task2 = Task(
            title="Task 2",
            description="Second task",
            users={user.id}
        )
        repo.save(task1)
        repo.save(task2)
        tasks = repo.list()
        assert len(tasks) == 2
        titles = {t.title for t in tasks}
        assert "Task 1" in titles
        assert "Task 2" in titles