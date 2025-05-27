import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from uuid import UUID

from src.core._shared.notification import Notification


@dataclass(kw_only=True)
class Entity(ABC):
    """Base class for all entities in the domain model."""

    id: UUID = field(default_factory=uuid.uuid4)
    notification: Notification = field(default_factory=Notification)

    def __eq__(self, value):
        if not isinstance(value, self.__class__):
            return False
        return self.id == value.id

    @abstractmethod
    def validate(self) -> None:
        """Validate the entity. Should be implemented by subclasses."""
        pass
