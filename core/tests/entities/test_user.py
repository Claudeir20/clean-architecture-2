import unittest
from core.domain.entities.user import User, PermissionError

class TestUser(unittest.TestCase):
    def test_user_initialization(self):
        user = User(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            is_active=True,
            is_staff=False,
            is_superuser=False
        )
        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_is_admin_staff_and_superuser(self):
        user = User(email="admin@example.com", first_name="Admin", last_name="User", is_staff=True, is_superuser=True)
        self.assertTrue(user.is_admin())

    def test_is_admin_not_staff(self):
        user = User(email="user@example.com", first_name="User", last_name="Test", is_staff=False, is_superuser=True)
        self.assertFalse(user.is_admin())

    def test_is_admin_not_superuser(self):
        user = User(email="staff@example.com", first_name="Staff", last_name="Test", is_staff=True, is_superuser=False)
        self.assertFalse(user.is_admin())

    def test_can_manager_products_admin(self):
        user = User(email="admin@example.com", first_name="Admin", last_name="User", is_staff=True, is_superuser=True)
        self.assertTrue(user.can_manager_products())

    def test_can_manager_products_non_admin(self):
        user = User(email="user@example.com", first_name="User", last_name="Test", is_staff=False, is_superuser=False)
        with self.assertRaises(PermissionError) as context:
            user.can_manager_products()
        self.assertIn("Apenas administradores podem gerenciar produtos", str(context.exception))

    def test_can_view_orders_owner(self):
        user = User(email="owner@example.com", first_name="Owner", last_name="Test")
        self.assertTrue(user.can_view_orders(user.id))

    def test_can_view_orders_admin(self):
        admin = User(email="admin@example.com", first_name="Admin", last_name="Test", is_staff=True, is_superuser=True)
        other_id = "other_user_id"
        self.assertTrue(admin.can_view_orders(other_id))

    def test_can_view_orders_other_non_admin(self):
        user = User(email="user@example.com", first_name="User", last_name="Test")
        other_id = "other_user_id"
        self.assertFalse(user.can_view_orders(other_id))

    def test_eq_by_id(self):
        user1 = User(email="test@example.com", first_name="John", last_name="Doe")
        user2 = User(email="test@example.com", first_name="John", last_name="Doe")
        user1.id = "same_id"
        user2.id = "same_id"
        self.assertEqual(user1, user2)

    def test_eq_different_id(self):
        user1 = User(email="test1@example.com", first_name="John", last_name="Doe")
        user2 = User(email="test2@example.com", first_name="Jane", last_name="Doe")
        self.assertNotEqual(user1, user2)

    def test_hash_by_id(self):
        user = User(email="test@example.com", first_name="John", last_name="Doe")
        self.assertEqual(hash(user), hash(user.id))

    def test_str_representation(self):
        user = User(email="test@example.com", first_name="John", last_name="Doe")
        expected = f"User(id={user.id}), email=(test@example.com)"
        self.assertEqual(str(user), expected)

if __name__ == '__main__':
    unittest.main()
