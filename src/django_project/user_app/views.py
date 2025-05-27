from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from src.adapters.hash.bcrypt_adapter import BcryptAdapter

from src.core.user.application.exceptions import UserAlreadyExists, UserNotFound
from src.core.user.application.use_cases.create_user import CreateUser

from src.django_project.user_app.repository import DjangoORMUserRepository
from src.django_project.user_app.serializers import (
    CreateUserRequestSerializer,
    UserResponseSerializer,
)

class UserViewSet(viewsets.ViewSet):

    @staticmethod
    def create(request: Request) -> Response:
        """Create a new user."""
        serializer = CreateUserRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = CreateUser(
            repository=DjangoORMUserRepository(),
            password_hasher=BcryptAdapter(),
        )
        response = use_case.execute(
            request=CreateUser.CreateUserRequest(
                **serializer.validated_data
            )
        )

        response_serializer = UserResponseSerializer(response)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )