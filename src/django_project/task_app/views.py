from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


from src.core.tasks.application.use_cases.create_task import CreateTask
from src.core.tasks.application.exceptions import InvalidTaskData, RelatedUserNotFound, InvalidTaskBy
from src.django_project.task_app.serializers import CreateTaskRequestSerializer, CreateTaskResponseSerializer, TaskListResponseSerializer

from src.core.tasks.application.use_cases.list_task import ListTask

from src.django_project.task_app.repository import DjangoOrmTaskRepository
from src.django_project.user_app.repository import DjangoORMUserRepository
from src.django_project.auth_app.views import JWTAuthentication



class TaskViewSet(viewsets.ViewSet):
    """
    A viewset for managing tasks.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    
    def list(self, request):
        order_by = request.query_params.get('order_by', 'title')
        page = int(request.query_params.get('page', 1))
        size = int(request.query_params.get('size', 10))

        use_case = ListTask(
            repository=DjangoOrmTaskRepository(),
        )
        request_uc = ListTask.ListTaskRequest(
            order_by=order_by,
            page=page,
            size=size,
            user_id=str(request.user.id)
        )
        try:
            response = use_case.execute(request=request_uc)
        except (InvalidTaskData, RelatedUserNotFound) as err:
            return Response(
                {"error": str(err)},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = TaskListResponseSerializer(instance=response)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

    def create(self, request: Request) -> Response:
        serializer = CreateTaskRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data.copy()
        user_ids = set(data.get('users', []))
        user_ids.add(request.user.id)
        data['user_ids'] = user_ids
        data.pop('users', None)

        use_case = CreateTask(
            repository=DjangoOrmTaskRepository(),
            user_repository=DjangoORMUserRepository()
        )
        try:
            input_data = CreateTask.CreateTaskRequest(**data)
            response = use_case.execute(request=input_data)
        except (InvalidTaskData, RelatedUserNotFound) as err:
            return Response(
                {"error": str(err)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            CreateTaskResponseSerializer(response).data,
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific task by its ID.
        """
        # Logic to retrieve a task by its ID
        pass

    def update(self, request, pk=None):
        """
        Update an existing task.
        """
        # Logic to update a task by its ID
        pass

    def destroy(self, request, pk=None):
        """
        Delete a specific task.
        """
        # Logic to delete a task by its ID
        pass
