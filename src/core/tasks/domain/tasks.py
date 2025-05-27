from uuid import UUID
from dataclasses import dataclass, field
from enum import StrEnum
from datetime import datetime

from src.core._shared.entity import Entity

class TaskStatus(StrEnum):
    COMPLETED = "completed"
    PENDING = "pending"

@dataclass
class Task(Entity):
    title: str
    description: str
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime = None
    status: TaskStatus = field(default=TaskStatus.PENDING)
    users: set[UUID] = field(default_factory=set)

    def __post_init__(self):
        self.validate()

    def validate(self):
        if not self.title:
            self.notification.add_error("Title cannot be empty.")
        if not self.description:
            self.notification.add_error("Description cannot be empty.")
        if self.completed_at and not self.completed:
            self.notification.add_error("Task cannot be completed without setting completed at date.")
        if self.completed and not self.completed_at:
            self.notification.add_error("Completed tasks must have a completed at date set.")
        if self.completed_at and self.status != TaskStatus.COMPLETED:
            self.notification.add_error("Completed tasks must have a status of 'completed'.")
        if len(self.users) > 10:
            self.notification.add_error("A task cannot have more than 10 users assigned.")
        if len(self.title) > 30:
            self.notification.add_error("Title cannot exceed 30 characters.")
        if len(self.description) > 255:
            self.notification.add_error("Description cannot exceed 255 characters.")
        if self.notification.has_errors():
            raise ValueError("Task validation failed: " + ", ".join(self.notification.get_errors()))

    def __str__(self):
        return f"{self.title} - {self.status.value} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    def __repr__(self):
        return f"Task(title={self.title}, status={self.status.value}, created_at={self.created_at})"

    def complete_task(self):
        self.completed = True
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()
        self.validate()

    def add_user(self, user_id: UUID):
        if user_id in self.users:
            raise ValueError("User is already assigned to this task.")
        self.users.add(user_id)
        self.updated_at = datetime.now()
        self.validate()

    def remove_user(self, user_id: UUID):
        if user_id not in self.users:
            raise ValueError("User is not assigned to this task.")
        self.users.remove(user_id)
        self.updated_at = datetime.now()
        self.validate()

    def update_task(self, title: str = None, description: str = None):
        if title:
            self.title = title
        if description:
            self.description = description
        self.updated_at = datetime.now()
        self.validate()