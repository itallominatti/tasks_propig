from dataclasses import dataclass


@dataclass
class Notification:
    def __init__(self):
        self.errors: list[dict] = []

    def add_error(self, error: dict) -> None:
        """Add an error to the notification."""
        self.errors.append(error)

    def has_errors(self) -> bool:
        """Check if there are any errors in the notification."""
        return len(self.errors) > 0

    def get_errors(self) -> list[dict]:
        """Get the list of errors."""
        return self.errors

    @property
    def messages(self) -> str:
        """Get a string representation of the errors."""
        return "\n".join(
            [f"{error['code']}: {error['message']}" for error in self.errors]
        )
