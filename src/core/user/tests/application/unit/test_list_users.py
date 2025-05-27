from unittest.mock import MagicMock
import pytest

from src.core.user.domain.user_repository_interface import UserRepositoryInterface
from src.core.user.application.use_cases.list_users import ListUsers

from src.core.user.application.exceptions import InvalidOrderBy

from src.core.user.domain.user import User

class TestListUsers:
    def test_list_users_with_valid_order_by(self):
        mock_repository = MagicMock(UserRepositoryInterface)
        mock_repository.list.return_value = [
            User(username="alice", email="alice@gmail.com", password="securepassword123"),
            User(username="bob", email="bob@gmail.com", password="securepassword123"),
            User(username="charlie", email="charlie@gmail.com", password="securepassword123")
        ]
        use_case = ListUsers(repository=mock_repository)
        request = ListUsers.ListUsersRequest(order_by="username", current_page=1, page_size=2)
        response = use_case.execute(request)
        assert isinstance(response, ListUsers.ListUsersResponse)
        assert len(response.data) == 2
        assert response.meta.total_users == 3
        assert response.meta.current_page == 1
        assert response.meta.page_size == 2
        assert response.data[0].username == "alice"
        assert response.data[1].username == "bob"

    def test_list_users_with_invalid_order_by(self):
        mock_repository = MagicMock(UserRepositoryInterface)
        mock_repository.list.return_value = [
            User(username="alice", email="alice@gmail.com", password="securepassword123"),
            User(username="bob", email="bob@gmail.com", password="securepassword123"),
            User(username="charlie", email="charlie@gmail.com", password="securepassword123")
        ]
        use_case = ListUsers(repository=mock_repository)
        request = ListUsers.ListUsersRequest(order_by="abobora", current_page=1, page_size=2)
        with pytest.raises(InvalidOrderBy):
            use_case.execute(request)
        
    def test_list_users_with_pagination(self):
        mock_repository = MagicMock(UserRepositoryInterface)
        mock_repository.list.return_value = [
            User(username="alice", email="alice@gmail.com", password="securepassword123"),
            User(username="bob", email="bob@gmail.com", password="securepassword123"),
            User(username="charlie", email="charlie@gmail.com", password="securepassword123"),
            User(username="dave", email="dave@gmail.com", password="securepassword123"),
            User(username="eve", email="eve@gmail.com", password="securepassword123"),
            User(username="frank", email="frank@gmail.com", password="securepassword123")
        ]
        use_case = ListUsers(repository=mock_repository)
        request = ListUsers.ListUsersRequest(order_by="username", current_page=2, page_size=2)
        response = use_case.execute(request)
        assert isinstance(response, ListUsers.ListUsersResponse)
        assert len(response.data) == 2
        assert response.meta.total_users == 6
        assert response.meta.current_page == 2
        assert response.meta.page_size == 2
        assert response.data[0].username == "charlie"
        assert response.data[1].username == "dave"

    def test_list_users_with_empty_repository(self):
        mock_repository = MagicMock(UserRepositoryInterface)
        mock_repository.list.return_value = []
        use_case = ListUsers(repository=mock_repository)
        request = ListUsers.ListUsersRequest(order_by="username", current_page=1, page_size=10)
        response = use_case.execute(request)
        assert isinstance(response, ListUsers.ListUsersResponse)
        assert len(response.data) == 0
        assert response.meta.total_users == 0
        assert response.meta.current_page == 1
        assert response.meta.page_size == 10

    def test_list_users_with_single_user(self):
        mock_repository = MagicMock(UserRepositoryInterface)
        mock_repository.list.return_value = [
            User(username="alice", email="alice@gmail.com", password="securepassword123")
        ]
        use_case = ListUsers(repository=mock_repository)
        request = ListUsers.ListUsersRequest(order_by="username", current_page=1, page_size=10)
        response = use_case.execute(request)
        assert isinstance(response, ListUsers.ListUsersResponse)
        assert len(response.data) == 1
        assert response.meta.total_users == 1
        assert response.meta.current_page == 1
        assert response.meta.page_size == 10
        assert response.data[0].username == "alice"