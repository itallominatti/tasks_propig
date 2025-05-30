from typing import List, Optional
from src.core.user.domain.user_repository_interface import UserRepositoryInterface
from src.core.user.domain.user import User

class InMemoryUserRepository(UserRepositoryInterface):
    """In-memory implementation of the UserRepositoryInterface."""

    def __init__(self, users=None) -> None:
        self.users = users or []

    def save(self, user) -> None:
        """Save a user to the in-memory repository."""
        self.users.append(user)

    def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        for user in self.users:
            if user.email == email:
                return user
        return None

    def list(self) -> List[User]:
        return [user for user in self.users]

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by their unique identifier."""
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        return next((user for user in self.users if user.username == username), None)