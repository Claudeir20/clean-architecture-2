import unittest
from unittest.mock import Mock
from core.interfaces.usecase.criar_user_usecase import (
    CreateUserUseCase, CreateUserRequest, CreateUserResponse,
    ListUsersUseCase, ListUsersRequest, ListUsersResponse,
    GetUserByIdUseCase, GetUserByIdRequest,
    GetUserByEmailUseCase, GetUserByEmailRequest
)
from core.domain.entities.user import User

class TestCreateUserUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        self.use_case = CreateUserUseCase(self.mock_repo)

    def test_execute_success(self):
        request = CreateUserRequest(
            email="newuser@example.com",
            first_name="New",
            last_name="User",
            is_active=True,
            is_staff=False,
            is_superuser=False
        )
        created_user = User(
            id="user123",
            email="newuser@example.com",
            first_name="New",
            last_name="User",
            is_active=True,
            is_staff=False,
            is_superuser=False
        )
        self.mock_repo.create.return_value = created_user

        response = self.use_case.execute(request)

        self.assertIsInstance(response, CreateUserResponse)
        self.assertEqual(response.id, "user123")
        self.assertEqual(response.email, "newuser@example.com")
        self.assertEqual(response.first_name, "New")
        self.assertEqual(response.last_name, "User")
        self.assertTrue(response.is_active)
        self.assertFalse(response.is_staff)
        self.assertFalse(response.is_superuser)
        self.mock_repo.create.assert_called_once()

class TestListUsersUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        self.use_case = ListUsersUseCase(self.mock_repo)

    def test_execute_success(self):
        request = ListUsersRequest(offset=0, limit=10, search_query="test")
        users = [
            User(id="1", email="user1@example.com", first_name="User1", last_name="Test", is_active=True, is_staff=False, is_superuser=False),
            User(id="2", email="user2@example.com", first_name="User2", last_name="Test", is_active=True, is_staff=False, is_superuser=False)
        ]
        self.mock_repo.get_all_paginated_filtered.return_value = (users, 2)

        response = self.use_case.execute(request)

        self.assertIsInstance(response, ListUsersResponse)
        self.assertEqual(len(response.users), 2)
        self.assertEqual(response.total_items, 2)
        self.assertEqual(response.users[0].id, "1")
        self.mock_repo.get_all_paginated_filtered.assert_called_once_with(offset=0, limit=10, search_query="test")

class TestGetUserByIdUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        self.use_case = GetUserByIdUseCase(self.mock_repo)

    def test_execute_success(self):
        request = GetUserByIdRequest(user_id="user123")
        user = User(id="user123", email="user@example.com", first_name="User", last_name="Test", is_active=True, is_staff=False, is_superuser=False)
        self.mock_repo.get_by_id.return_value = user

        response = self.use_case.execute(request)

        self.assertIsInstance(response, CreateUserResponse)
        self.assertEqual(response.id, "user123")
        self.assertEqual(response.email, "user@example.com")
        self.mock_repo.get_by_id.assert_called_once_with("user123")

class TestGetUserByEmailUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        self.use_case = GetUserByEmailUseCase(self.mock_repo)

    def test_execute_found(self):
        request = GetUserByEmailRequest(user_email="user@example.com")
        user = User(id="user123", email="user@example.com", first_name="User", last_name="Test", is_active=True, is_staff=False, is_superuser=False)
        self.mock_repo.get_by_email.return_value = user

        response = self.use_case.execute(request)

        self.assertIsInstance(response, CreateUserResponse)
        self.assertEqual(response.id, "user123")
        self.assertEqual(response.email, "user@example.com")
        self.mock_repo.get_by_email.assert_called_once()

    def test_execute_not_found(self):
        request = GetUserByEmailRequest(user_email="nonexistent@example.com")
        self.mock_repo.get_by_email.return_value = None

        with self.assertRaises(ValueError) as context:
            self.use_case.execute(request)
        self.assertIn("Usuário não encontrado", str(context.exception))
        self.mock_repo.get_by_email.assert_called_once()

if __name__ == '__main__':
    unittest.main()
