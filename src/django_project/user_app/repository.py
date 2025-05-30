from uuid import UUID
from typing import Optional

from src.core.user.domain.user import User
from src.core.user.domain.user_repository_interface import UserRepositoryInterface

from src.django_project.user_app.models import User as DjangoUserModel

class DjangoORMUserRepository(UserRepositoryInterface):
    """Django ORM implementation of the UserRepositoryInterface."""

    def __init__(self, user_model: DjangoUserModel = DjangoUserModel) -> None:
        self.user_model = user_model

    def save(self, user: User) -> User:
        """Save a user entity to the database."""
        user_orm = UserModelMapper.to_model(user)
        user_orm.save()

    def get_by_email(self, email: str) -> User | None:
        """Get a user by email."""
        try:
            user_model = self.user_model.objects.get(email=email)
            return UserModelMapper.to_entity(user_model)
        except self.user_model.DoesNotExist:
            return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        try:
            user_model = self.user_model.objects.get(username=username)
            return UserModelMapper.to_entity(user_model)
        except self.user_model.DoesNotExist:
            return None

        
    def list(self, user_id: UUID = None) -> list[User]:
        queryset = self.user_model.objects.all()
        if user_id is not None:
            queryset = queryset.filter(id=user_id)
        return [UserModelMapper.to_entity(user_model) for user_model in queryset]

    
    def get_user_by_id(self, user_id: UUID) -> User | None:
        """Get a user by their unique identifier."""
        try:
            user_model = self.user_model.objects.get(id=user_id)
            return UserModelMapper.to_entity(user_model)
        except self.user_model.DoesNotExist:
            return None
        
class UserModelMapper:
    @staticmethod
    def to_model(user: User) -> DjangoUserModel:
        """Convert a User domain entity to a Django ORM model."""
        return DjangoUserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            password=user.password,
        )
    @staticmethod
    def to_entity(user_model: DjangoUserModel) -> User:
        """Convert a Django ORM model to a User domain entity."""
        return User(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            password=user_model.password,
        )
    
        