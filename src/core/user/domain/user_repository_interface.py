from abc import ABC, abstractmethod
from typing import List, Optional
from src.core.user.domain.user import User

class UserRepositoryInterface(ABC):
    @abstractmethod
    def save(self, user) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        raise NotImplementedError

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by their username."""
        raise NotImplementedError