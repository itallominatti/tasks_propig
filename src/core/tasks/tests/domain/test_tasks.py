import uuid
from uuid import UUID
from datetime import datetime

import pytest

from src.core.tasks.domain.tasks import Task, TaskStatus

class TestTask:
    def test_create_task_with_empty_title(self):
        with pytest.raises(ValueError, match="Title cannot be empty."):
            Task(title="", description="desc")

    def test_create_task_with_empty_description(self):
        with pytest.raises(ValueError, match="Description cannot be empty."):
            Task(title="Task 1", description="")

    def test_create_task_with_long_title(self):
        with pytest.raises(ValueError, match="Title cannot exceed 30 characters."):
            Task(title="a" * 31, description="desc")

    def test_create_task_with_long_description(self):
        with pytest.raises(ValueError, match="Description cannot exceed 255 characters."):
            Task(title="Task 1", description="a" * 256)

    def test_create_task_with_too_many_users(self):
        users = {uuid.uuid4() for _ in range(11)}
        with pytest.raises(ValueError, match="A task cannot have more than 10 users assigned."):
            Task(title="Task 1", description="desc", users=users)

    def test_complete_task_without_completed_at(self):
        task = Task(title="Task 1", description="desc")
        # Força completed=True sem completed_at
        task.completed = True
        task.completed_at = None
        with pytest.raises(ValueError, match="Completed tasks must have a completed at date set."):
            task.validate()

    def test_completed_at_without_completed(self):
        task = Task(title="Task 1", description="desc")
        task.completed = False
        task.completed_at = datetime.now()
        with pytest.raises(ValueError, match="Task cannot be completed without setting completed at date."):
            task.validate()

    def test_add_user_already_assigned(self):
        user_id = uuid.uuid4()
        task = Task(title="Task 1", description="desc", users={user_id})
        with pytest.raises(ValueError, match="User is already assigned to this task."):
            task.add_user(user_id)

    def test_remove_user_not_assigned(self):
        user_id = uuid.uuid4()
        task = Task(title="Task 1", description="desc")
        with pytest.raises(ValueError, match="User is not assigned to this task."):
            task.remove_user(user_id)

    def test_create_valid_task(self):
        task = Task(title="Task 1", description="desc")
        assert isinstance(task, Task)
        assert task.status == TaskStatus.PENDING
        assert not task.completed