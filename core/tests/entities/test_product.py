import unittest
from core.domain.entities.product import Product

class TestProduct(unittest.TestCase):
    def test_product_initialization(self):
        product = Product(name="Test Product", price=15.5, stock=50, is_active=True)
        self.assertIsNotNone(product.id)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, 15.5)
        self.assertEqual(product.stock, 50)
        self.assertTrue(product.is_active)

    def test_is_available_active_with_stock(self):
        product = Product(name="Available", price=10.0, stock=5, is_active=True)
        self.assertTrue(product.is_available())

    def test_is_available_inactive(self):
        product = Product(name="Inactive", price=10.0, stock=5, is_active=False)
        self.assertFalse(product.is_available())

    def test_is_available_no_stock(self):
        product = Product(name="No Stock", price=10.0, stock=0, is_active=True)
        self.assertFalse(product.is_available())

    def test_reduce_stock_success(self):
        product = Product(name="Stock Test", price=10.0, stock=10, is_active=True)
        product.reduce_stock(3)
        self.assertEqual(product.stock, 7)

    def test_reduce_stock_insufficient(self):
        product = Product(name="Low Stock", price=10.0, stock=2, is_active=True)
        with self.assertRaises(ValueError) as context:
            product.reduce_stock(5)
        self.assertIn("Estoque insuficicente", str(context.exception))
        self.assertEqual(product.stock, 2)  # Stock unchanged

if __name__ == '__main__':
    unittest.main()
