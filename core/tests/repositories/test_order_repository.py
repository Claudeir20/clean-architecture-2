import unittest
from core.domain.repositories.order_repository import OrderRepository

class TestOrderRepository(unittest.TestCase):
    def setUp(self):
        class ConcreteOrderRepository(OrderRepository):
            def create(self, order):
                raise NotImplementedError

            def get_all(self):
                raise NotImplementedError

            def get_by_owner_id(self, owner_id):
                raise NotImplementedError

            def get_by_order_id(self, order_id):
                raise NotImplementedError

        self.repo = ConcreteOrderRepository()

    def test_create_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.repo.create(None)

    def test_get_all_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.repo.get_all()

    def test_get_by_owner_id_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.repo.get_by_owner_id("owner_id")

    def test_get_by_order_id_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.repo.get_by_order_id("order_id")

if __name__ == '__main__':
    unittest.main()
