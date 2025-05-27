import uuid
import pytest
from datetime import datetime
from src.core.tasks.application.use_cases.get_task import GetTask, TaskOutput
from src.core.tasks.application.exceptions import TaskNotFound

class FakeTask:
    def __init__(self, id, title, description, status, created_at, updated_at, users):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.users = users

class FakeRepo:
    def __init__(self, task=None):
        self._task = task
    def get_by_id(self, task_id):
        if self._task and self._task.id == task_id:
            return self._task
        return None

def make_task():
    return FakeTask(
        id=uuid.uuid4(),
        title="Test Task",
        description="A test task",
        status="pending",
        created_at=datetime(2024, 1, 1, 12, 0, 0),
        updated_at=datetime(2024, 1, 2, 12, 0, 0),
        users={uuid.uuid4()}
    )

def test_get_task_success():
    task = make_task()
    repo = FakeRepo(task)
    use_case = GetTask(repo)
    request = GetTask.GetTaskRequest(task_id=task.id)
    response = use_case.execute(request)
    assert isinstance(response.data, TaskOutput)
    assert response.data.id == task.id
    assert response.data.title == "Test Task"
    assert response.data.status == "pending"
    assert "self" in response.data.links
    assert "delete" in response.data.links
    assert "update" in response.data.links
    assert "patch" in response.data.links
    assert "create" in response.data.links

def test_get_task_not_found():
    repo = FakeRepo()
    use_case = GetTask(repo)
    request = GetTask.GetTaskRequest(task_id=uuid.uuid4())
    with pytest.raises(TaskNotFound):
        use_case.execute(request)

def test_get_task_links_structure():
    task = make_task()
    repo = FakeRepo(task)
    use_case = GetTask(repo)
    request = GetTask.GetTaskRequest(task_id=task.id)
    response = use_case.execute(request)
    links = response.data.links
    assert links["self"] == f"/api/tasks/{task.id}"
    assert links["delete"]["href"] == f"/api/tasks/{task.id}"
    assert links["update"]["href"] == f"/api/tasks/{task.id}"
    assert links["patch"]["href"] == f"/api/tasks/{task.id}"
    assert links["create"]["href"] == "/api/tasks"