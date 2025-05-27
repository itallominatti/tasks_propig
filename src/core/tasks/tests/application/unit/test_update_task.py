import uuid
from unittest.mock import create_autospec
import pytest

from src.core.tasks.application.use_cases.update_task import UpdateTask
from src.core.tasks.application.exceptions import TaskNotFound
from src.core.tasks.domain.task_repository_interface import TaskRepositoryInterface
from src.core.tasks.domain.tasks import Task, TaskStatus

@pytest.fixture
def mock_task_repository():
    return create_autospec(TaskRepositoryInterface)

@pytest.fixture
def existing_task():
    return Task(
        id=uuid.uuid4(),
        title="Old Title",
        description="Old Description",
        status=TaskStatus.PENDING,
        users=set()
    )

class TestUpdateTask:
    def test_when_task_does_not_exist_then_raise_task_not_found(self, mock_task_repository):
        mock_task_repository.get_by_id.return_value = None
        use_case = UpdateTask(mock_task_repository)
        request = UpdateTask.UpdateTaskRequest(
            task_id=uuid.uuid4(),
            title="New Title",
            description="New Desc",
            status=TaskStatus.COMPLETED
        )
        with pytest.raises(TaskNotFound):
            use_case.execute(request)

    def test_update_title_and_description(self, mock_task_repository, existing_task):
        mock_task_repository.get_by_id.return_value = existing_task
        use_case = UpdateTask(mock_task_repository)
        request = UpdateTask.UpdateTaskRequest(
            task_id=existing_task.id,
            title="New Title",
            description="New Description",
            status=None
        )
        use_case.execute(request)
        assert existing_task.title == "New Title"
        assert existing_task.description == "New Description"
        assert existing_task.status == TaskStatus.PENDING
        mock_task_repository.save.assert_called_once_with(existing_task)

    def test_update_status_only(self, mock_task_repository, existing_task):
        mock_task_repository.get_by_id.return_value = existing_task
        use_case = UpdateTask(mock_task_repository)
        request = UpdateTask.UpdateTaskRequest(
            task_id=existing_task.id,
            status=TaskStatus.COMPLETED
        )
        use_case.execute(request)
        assert existing_task.status == TaskStatus.COMPLETED
        mock_task_repository.save.assert_called_once_with(existing_task)

    def test_update_partial_fields(self, mock_task_repository, existing_task):
        mock_task_repository.get_by_id.return_value = existing_task
        use_case = UpdateTask(mock_task_repository)
        request = UpdateTask.UpdateTaskRequest(
            task_id=existing_task.id,
            title=None,
            description="Only Description Updated",
            status=None
        )
        use_case.execute(request)
        assert existing_task.title == "Old Title"
        assert existing_task.description == "Only Description Updated"
        mock_task_repository.save.assert_called_once_with(existing_task)