from django.contrib import admin

from django.urls import path


from rest_framework.routers import DefaultRouter
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from src.django_project.user_app.views import UserViewSet
from src.django_project.task_app.views import TaskViewSet
from src.django_project.auth_app.views import AuthenticateUserView

schema_view = get_schema_view(
    openapi.Info(
        title="Tasks Propig API",
        default_version="v1",
        description="API documentation for Tasks Propig"
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(prefix=r"api/users", viewset=UserViewSet, basename="users")
router.register(prefix=r"api/tasks", viewset=TaskViewSet, basename="tasks")

urlpatterns = [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("admin/", admin.site.urls),
    path('auth/login/', AuthenticateUserView.as_view(), name='auth-login'),
] + router.urls
