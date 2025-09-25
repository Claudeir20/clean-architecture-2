import unittest
from core.domain.repositories.user_repository import UserRepository

class TestUserRepository(unittest.TestCase):
    def setUp(self):
        class ConcreteUserRepository(UserRepository):
            def create(self, user):
                raise NotImplementedError

            def get_all(self, user):
                raise NotImplementedError

            def get_by_id(self, user_id):
                raise NotImplementedError

            def get_by_email(self, user):
                raise NotImplementedError

            def get_all_paginated_filtered(self, offset, limit, search_query):
                raise NotImplementedError

        self.repo = ConcreteUserRepository()

    def test_create_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.repo.create(None)

    def test_get_all_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.repo.get_all(None)

    def test_get_by_id_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.repo.get_by_id("user_id")

    def test_get_by_email_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.repo.get_by_email(None)

    def test_get_all_paginated_filtered_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.repo.get_all_paginated_filtered(0, 10, None)

if __name__ == '__main__':
    unittest.main()
