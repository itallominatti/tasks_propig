import uuid
import pytest
from datetime import datetime

from src.core.tasks.domain.tasks import Task, TaskStatus
from src.core.tasks.infra.in_memory_task_repository import InMemoryTaskRepository

@pytest.fixture
def repo():
    return InMemoryTaskRepository()

@pytest.fixture
def user_id():
    return uuid.uuid4()

@pytest.fixture
def another_user_id():
    return uuid.uuid4()

@pytest.fixture
def task(user_id):
    return Task(
        title="Test Task",
        description="A test task",
        users={user_id}
    )

def test_save_and_get_by_id(repo, task):
    repo.save(task)
    found = repo.get_by_id(task.id)
    assert found is not None
    assert found.title == "Test Task"

def test_update_task(repo, task):
    repo.save(task)
    task.update_task(title="Updated Title")
    repo.update(task)
    found = repo.get_by_id(task.id)
    assert found.title == "Updated Title"

def test_delete_task(repo, task):
    repo.save(task)
    repo.delete(task.id)
    assert repo.get_by_id(task.id) is None

def test_list_tasks(repo, task, user_id):
    repo.save(task)
    tasks = repo.list(user_id)
    assert len(tasks) == 1
    assert tasks[0].title == "Test Task"

def test_user_can_only_see_own_tasks(repo, user_id, another_user_id):
    task1 = Task(
        title="User Task",
        description="Task for user",
        users={user_id}
    )
    task2 = Task(
        title="Other User Task",
        description="Task for another user",
        users={another_user_id}
    )
    repo.save(task1)
    repo.save(task2)

    visible_tasks = repo.list(user_id)
    assert len(visible_tasks) == 1
    assert visible_tasks[0].title == "User Task"

    # Simula "listar tasks visíveis para another_user_id"
    visible_tasks_other = repo.list(another_user_id)
    assert len(visible_tasks_other) == 1
    assert visible_tasks_other[0].title == "Other User Task"

def test_user_cannot_see_task_if_not_in_users(repo, user_id, another_user_id):
    task = Task(
        title="Private Task",
        description="Should not be visible",
        users={another_user_id}
    )
    repo.save(task)
    visible_tasks = repo.list(user_id)
    assert len(visible_tasks) == 0