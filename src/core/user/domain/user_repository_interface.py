from abc import ABC, abstractmethod
from src.core.user.domain.user import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    def save(self, user) -> None:
        """Save a user to the repository."""
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> "User | None":
        """Get a user by email."""
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[User]:
        """Get a list of users."""
        raise NotImplementedError

