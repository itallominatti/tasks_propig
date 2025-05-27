from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from src.core.user.application.use_cases.authenticate_user import AuthenticateUser
from src.django_project.user_app.repository import DjangoORMUserRepository
from src.adapters.jwt.jwt_adapter import JWTAdapter
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
import jwt
from src.django_project.user_app.models import User

from src.django_project.auth_app.serializers import AuthenticateUserRequestSerializer, AuthenticateUserResponseSerializer


class AuthenticateUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthenticateUserRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = AuthenticateUser(
            repository=DjangoORMUserRepository(),
            jwt_adapter=JWTAdapter(secret_key=settings.SECRET_KEY)
        )
        try:
            response = use_case.execute(
                AuthenticateUser.AuthenticateUserRequest(**serializer.validated_data)
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        response_serializer = AuthenticateUserResponseSerializer(response)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        return (user, None)