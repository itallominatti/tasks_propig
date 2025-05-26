from uuid import uuid4, UUID
from dataclasses import dataclass, field
import re

from src.core._shared.entity import Entity

@dataclass
class User(Entity):
    """User entity representing a user in the system."""

    username: str = field(default="")
    email: str = field(default="")
    password: str = field(default="")
    is_active: bool = field(default=True)

    def __post_init__(self):
        """Post-initialization to validate the user entity."""
        self.validate()

    def validate(self) -> None:
        """Validate the user entity."""

        if not self.username:
            self.notification.add_error({"code": "username_required", "message": "Username is required."})

        if not self.email:
            self.notification.add_error({"code": "email_required", "message": "Email is required."})

        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            self.notification.add_error({"code": "email_invalid", "message": "Email is invalid."})

        if not self.password:
            self.notification.add_error({"code": "password_required", "message": "Password is required."})

        if not re.search(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', self.password):
            self.notification.add_error({"code": "password_invalid", "message": "Password must be at least 8 characters long and contain both letters and numbers."})
        
        if not isinstance(self.is_active, bool):
            self.notification.add_error({"code": "is_active_invalid", "message": "is_active must be a boolean value."})


        if self.notification.has_errors():
            raise ValueError(self.notification.messages)
        
    def activate(self) -> None:
        """Activate the user."""
        self.is_active = True
        self.validate()

    def deactivate(self) -> None:
        """Deactivate the user."""
        self.is_active = False
        self.validate()

    
