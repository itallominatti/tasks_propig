import uuid
from unittest.mock import create_autospec

import pytest

from src.core.user.domain.user_repository_interface import UserRepositoryInterface
from src.core.tasks.application.exceptions import RelatedUserNotFound, InvalidTaskData
from src.core.tasks.application.use_cases.create_task import CreateTask
from src.core.tasks.domain.task_repository_interface import TaskRepositoryInterface

from src.core.tasks.domain.tasks import Task
from src.core.user.domain.user import User

@pytest.fixture
def mock_task_repository():
    return create_autospec(TaskRepositoryInterface)

@pytest.fixture
def mock_user_repository():
    return create_autospec(UserRepositoryInterface)

@pytest.fixture
def task_move_card() -> Task:
    return Task(
        id=uuid.uuid4(),
        title="Task Mover Card",
        description="A task to move a card",
        users=set()
    )

@pytest.fixture
def task_finish_card() -> Task:
    return Task(
        id=uuid.uuid4(),
        title="Task Finish Card",
        description="A task to finish a card",
        users=set()
    )

@pytest.fixture
def mock_user_repository_with_users(mock_user_repository):
    user1 = User(id=uuid.uuid4(), username="User1", email="user1@gmail.com", password="securepassword123")
    user2 = User(id=uuid.uuid4(), username="User2", email="user2@gmail.com", password="securepassword123")
    mock_user_repository.list.return_value = [user1, user2]
    return mock_user_repository

@pytest.fixture
def mock_empty_user_repository(mock_user_repository):
    mock_user_repository.list.return_value = []
    return mock_user_repository

class TestCreateTask:
    def test_when_users_do_not_exist_then_raise_related_user_not_found(
        self, mock_task_repository, mock_empty_user_repository
    ):
        create_task = CreateTask(mock_task_repository, mock_empty_user_repository)

        request = CreateTask.CreateTaskRequest(
            title="Test Task",
            description="This is a test task",
            user_ids={uuid.uuid4()}
        )

        with pytest.raises(RelatedUserNotFound):
            create_task.execute(request)

    def test_when_task_data_is_invalid_then_raise_invalid_task_data(
        self, mock_task_repository, mock_user_repository_with_users
    ):
        create_task = CreateTask(mock_task_repository, mock_user_repository_with_users)

        valid_user_id = mock_user_repository_with_users.list.return_value[0].id

        request = CreateTask.CreateTaskRequest(
            title="",
            description="This is a test task",
            user_ids={valid_user_id}
        )

        with pytest.raises(InvalidTaskData):
            create_task.execute(request)

    def test_when_task_is_created_successfully_then_return_create_task_response(
        self, mock_task_repository, mock_user_repository_with_users
    ):
        create_task = CreateTask(mock_task_repository, mock_user_repository_with_users)

        valid_user_id = mock_user_repository_with_users.list.return_value[0].id

        request = CreateTask.CreateTaskRequest(
            title="Test Task",
            description="This is a test task",
            user_ids={valid_user_id}
        )

        response = create_task.execute(request)

        assert isinstance(response, CreateTask.CreateTaskResponse)
        assert isinstance(response.id, uuid.UUID)
        mock_task_repository.save.assert_called_once()

    def test_when_task_is_created_with_multiple_users_then_return_create_task_response(
        self, mock_task_repository, mock_user_repository_with_users
    ):
        create_task = CreateTask(mock_task_repository, mock_user_repository_with_users)

        user_ids = {user.id for user in mock_user_repository_with_users.list.return_value}

        request = CreateTask.CreateTaskRequest(
            title="Test Task with Multiple Users",
            description="This is a test task with multiple users",
            user_ids=user_ids
        )

        response = create_task.execute(request)

        assert isinstance(response, CreateTask.CreateTaskResponse)
        assert isinstance(response.id, uuid.UUID)
        mock_task_repository.save.assert_called_once()