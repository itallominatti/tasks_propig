from src.core.user.domain.user import User
from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository


class TestInMemoryUserRepository:
    """Test suite for the InMemoryUserRepository."""

    def test_save_user(self):
        """Test saving a user to the in-memory repository."""
        repository = InMemoryUserRepository()
        user = User(
            username="testuser",
            email="teste@gmail.com",
            password="Senha123",
        )
        repository.save(user)

        assert len(repository.users) == 1
        assert repository.users[0] == user

    

    
