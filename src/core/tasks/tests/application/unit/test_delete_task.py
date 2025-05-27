import pytest
from uuid import uuid4
from unittest.mock import MagicMock

from src.core.tasks.application.use_cases.delete_task import DeleteTask, TaskNotFound, DeleteTask
from src.core.tasks.domain.tasks import Task

class DummyTask:
    pass

def test_delete_task_success():
    repo = MagicMock()
    task_id = uuid4()
    repo.get_by_id.return_value = DummyTask()
    delete_task = DeleteTask(repository=repo)
    request = DeleteTask.DeleteTaskRequest(id=task_id)

    delete_task.execute(request)

    repo.get_by_id.assert_called_once_with(str(task_id))
    repo.delete.assert_called_once_with(str(task_id))

def test_delete_task_not_found():
    repo = MagicMock()
    task_id = uuid4()
    repo.get_by_id.return_value = None
    delete_task = DeleteTask(repository=repo)
    request = DeleteTask.DeleteTaskRequest(id=task_id)

    with pytest.raises(TaskNotFound):
        delete_task.execute(request)