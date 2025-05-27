import pytest

from src.core.user.domain.user import User

from src.django_project.user_app.repository import DjangoORMUserRepository
from src.django_project.user_app.models import User as DjangoUserModel

@pytest.mark.django_db
class TestSave:
    def test_save_user_in_database(self):
        # Arrange
        user = User(
            username="testuser",
            email="testuser@gmail.com",
            password="securepassword123"
        )
        repository = DjangoORMUserRepository()

        assert DjangoUserModel.objects.count() == 0
        repository.save(user)
        assert DjangoUserModel.objects.count() == 1

        user_db = DjangoUserModel.objects.get()
        assert user_db.id == user.id
        assert user_db.username == user.username
        assert user_db.email == user.email
        assert user_db.password == user.password
 