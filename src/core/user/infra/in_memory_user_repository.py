from src.core.user.domain.user_repository_interface import UserRepositoryInterface
from src.core.user.domain.user import User


class InMemoryUserRepository(UserRepositoryInterface):
    """In-memory implementation of the UserRepositoryInterface."""

    def __init__(self, users=None) -> None:
        self.users = users or []

    def save(self, user) -> None:
        """Save a user to the in-memory repository."""
        self.users.append(user)

    def get_by_email(self, email: str) -> User | None:
        """Get a user by email."""
        for user in self.users:
            if user.email == email:
                return user
        return None
