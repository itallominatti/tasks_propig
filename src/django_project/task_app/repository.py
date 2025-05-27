from uuid import UUID

from src.core.tasks.domain.tasks import Task
from src.core.tasks.domain.task_repository_interface import TaskRepositoryInterface

from django.db import transaction

from src.django_project.task_app.models import Task as DjangoTaskModel
from src.django_project.user_app.models import User as DjangoUserModel

class DjangoOrmTaskRepository(TaskRepositoryInterface):
    """Django ORM implementation of the TaskRepositoryInterface."""

    def __init__(self, task_model: DjangoTaskModel = DjangoTaskModel) -> None:
        self.task_model = task_model

    def save(self, task: Task) -> Task:
        with transaction.atomic():
            task_orm = TaskModelMapper.to_model(task)
            task_orm.save()
            
            users_qs = DjangoUserModel.objects.filter(id__in=task.users)
            task_orm.users.set(users_qs)
            task_orm.save()
            return TaskModelMapper.to_entity(task_orm)

    def get_by_id(self, task_id: str) -> Task | None:
        try:
            task_model = self.task_model.objects.get(id=task_id)
            return TaskModelMapper.to_entity(task_model)
        except self.task_model.DoesNotExist:
            return None

    def delete(self, task_id: str) -> None:
        try:
            task_model = self.task_model.objects.get(id=task_id)
            task_model.delete()
        except self.task_model.DoesNotExist:
            pass

    def update(self, task: Task) -> Task:
        try:
            task_model = self.task_model.objects.get(id=task.id)
        except self.task_model.DoesNotExist:
            raise ValueError(f"Task with id {task.id} does not exist.")
        with transaction.atomic():
            task_model.title = task.title
            task_model.description = task.description
            task_model.updated_at = task.updated_at
            task_model.save()
            users_qs = DjangoUserModel.objects.filter(id__in=task.users)
            task_model.users.set(users_qs)
            task_model.save()
            return TaskModelMapper.to_entity(task_model)

    def list(self, user_id: UUID = None):
        queryset = self.task_model.objects.all()
        if user_id is not None:
            queryset = queryset.filter(users__id=user_id)
        return [TaskModelMapper.to_entity(task_model) for task_model in queryset]


class TaskModelMapper:
    @staticmethod
    def to_model(task: Task) -> DjangoTaskModel:
        return DjangoTaskModel(
            id=task.id,
            title=task.title,
            description=task.description,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )

    @staticmethod
    def to_entity(task_model: DjangoTaskModel) -> Task:
        return Task(
            id=task_model.id,
            title=task_model.title,
            description=task_model.description,
            created_at=task_model.created_at,
            updated_at=task_model.updated_at,
            users={user.id for user in task_model.users.all()},
        )