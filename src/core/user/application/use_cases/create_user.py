from uuid import UUID
from dataclasses import dataclass
import re

from src.adapters.hash.hash_adapter_interface import PasswordHasherInterface

from src.core.user.domain.user_repository_interface import UserRepositoryInterface
from src.core.user.domain.user import User
from src.core.user.application.exceptions import InvalidUser, UserAlreadyExists


class CreateUser:
    @dataclass
    class CreateUserRequest:
        username: str
        email: str
        password: str
        is_active: bool = True

    @dataclass
    class CreateUserResponse:
        id: UUID

    def __init__(
        self,
        repository: UserRepositoryInterface,
        password_hasher: PasswordHasherInterface,
    ) -> None:
        self.repository = repository
        self.password_hasher = password_hasher

    def execute(self, request: CreateUserRequest) -> CreateUserResponse:

        email_already_exists = self.repository.get_by_email(request.email)
        if email_already_exists:
            raise UserAlreadyExists(f"User with email {request.email} already exists.")

        try:
            if not re.search(
                r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", request.password
            ):
                raise InvalidUser(
                    "Password must be at least 8 characters long and contain both letters and numbers."
                )
            hashed_password = self.password_hasher.hash(request.password)
            user = User(
                username=request.username,
                email=request.email,
                password=hashed_password,
                is_active=request.is_active,
            )
        except ValueError as err:
            raise InvalidUser(err)
        self.repository.save(user=user)
        return self.CreateUserResponse(id=user.id)
