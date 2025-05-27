from abc import ABC, abstractmethod


class UserRepositoryInterface(ABC):
    @abstractmethod
    def save(self, user) -> None:
        """Save a user to the repository."""
        pass