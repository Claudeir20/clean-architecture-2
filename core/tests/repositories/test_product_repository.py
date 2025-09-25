import unittest
from core.domain.repositories.product_repository import ProductRepository

class TestProductRepository(unittest.TestCase):
    def setUp(self):
        class ConcreteProductRepository(ProductRepository):
            def create(self, product):
                raise NotImplementedError

            def get_all(self):
                raise NotImplementedError

            def get_by_id(self, product_id):
                raise NotImplementedError

            def get_all_paginated_filtered(self, offset, limit, search_query):
                raise NotImplementedError

        self.repo = ConcreteProductRepository()

    def test_create_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.repo.create(None)

    def test_get_all_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.repo.get_all()

    def test_get_by_id_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.repo.get_by_id("product_id")

    def test_get_all_paginated_filtered_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.repo.get_all_paginated_filtered(0, 10, None)

if __name__ == '__main__':
    unittest.main()
