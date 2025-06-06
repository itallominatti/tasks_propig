from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from src.adapters.hash.bcrypt_adapter import BcryptPasswordHasher

from src.core.user.application.exceptions import UserAlreadyExists, InvalidUser, UserNotFound
from src.core.user.application.use_cases.create_user import CreateUser
from src.core.user.application.use_cases.list_users import ListUsers, InvalidOrderBy
from src.core.user.application.use_cases.get_user import GetUser

from src.django_project.auth_app.views import JWTAuthentication

from src.django_project.user_app.repository import DjangoORMUserRepository
from src.django_project.user_app.serializers import (
    CreateUserRequestSerializer,
    CreateUserResponseSerializer,
    UserResponseSerializer,
    RetrieveUserRequestSerializer,
    UserResponseSerializer,
    RetrieveUserResponseSerializer,
)





class UserViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request: Request) -> Response:
        serializer = CreateUserRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        use_case = CreateUser(
            repository=DjangoORMUserRepository(),
            password_hasher=BcryptPasswordHasher(),
        )
        try:
            response = use_case.execute(
                request=CreateUser.CreateUserRequest(
                    **serializer.validated_data
                )
            )
        except (UserAlreadyExists, InvalidUser) as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response_serializer = CreateUserResponseSerializer(response)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )
    
    @staticmethod
    def list(request: Request) -> Response:
        use_case = ListUsers(repository=DjangoORMUserRepository())
        request_data = {
            "order_by": request.query_params.get("order_by", "username"),
            "current_page": int(request.query_params.get("page", 1)),
            "page_size": int(request.query_params.get("size", 10)),
        }

        try:
            response = use_case.execute(ListUsers.ListUsersRequest(**request_data))
        except InvalidOrderBy as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        users_serializer = UserResponseSerializer(response.data, many=True)
        
        meta = {
            "total_users": response.meta.total_users,
            "current_page": response.meta.current_page,
            "page_size": response.meta.page_size,
            "query_params": response.meta.query_params,
        }
        return Response(
            {
                "data": users_serializer.data,
                "meta": meta,
                "links": response.links,
            },
            status=status.HTTP_200_OK,
        )
    
    @staticmethod
    def retrieve(request: Request, pk=None) -> Response:
        serializer = RetrieveUserRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        use_case = GetUser(
            repository=DjangoORMUserRepository(),
        )
        try:
            response = use_case.execute(
                request=GetUser.GetUserRequest(
                    id=serializer.validated_data["id"]
                )
            )
        except (UserNotFound,InvalidUser) as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        response_serializer = RetrieveUserResponseSerializer(response)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )
