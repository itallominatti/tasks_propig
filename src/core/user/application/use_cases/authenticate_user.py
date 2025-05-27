from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from src.adapters.jwt.jwt_adapter import JWTAdapter

from src.adapters.hash.bcrypt_adapter import BcryptPasswordHasher
from src.adapters.hash.hash_adapter_interface import PasswordHasherInterface

from src.core.user.application.exceptions import InvalidUser
from src.django_project.user_app.repository import DjangoORMUserRepository


class AuthenticateUser:

    @dataclass
    class AuthenticateUserRequest:
        username: str
        password: str

    @dataclass
    class AuthenticateUserResponse:
        token: str
        expires_at: str

    def __init__(
            self,
            repository: DjangoORMUserRepository,
            jwt_adapter: JWTAdapter,
            token_exp_minutes: int = 60,
            hash_adapter: PasswordHasherInterface = BcryptPasswordHasher()
        ) -> None:
        self.repository = repository
        self.jwt_adapter = jwt_adapter
        self.token_exp_minutes = token_exp_minutes
        self.hash_adapter = hash_adapter

    def execute(self, request: AuthenticateUserRequest) -> AuthenticateUserResponse:
        user = self.repository.get_user_by_username(request.username)


        if not user or not user.check_password(request.password, self.hash_adapter):
            raise InvalidUser("Invalid username or password")

        expires_at = datetime.now(timezone.utc) + timedelta(minutes=self.token_exp_minutes)
        payload = {
            "user_id": str(user.id),
            "exp": int(expires_at.timestamp())
        }
        token = self.jwt_adapter.encode(payload)

        return self.AuthenticateUserResponse(
            token=token,
            expires_at=expires_at.replace(microsecond=0).isoformat().replace('+00:00', 'Z')
        )