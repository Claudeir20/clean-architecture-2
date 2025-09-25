import unittest
from core.domain.entities.order import Order
from core.domain.entities.product import Product

class TestOrder(unittest.TestCase):
    def setUp(self):
        self.product = Product(name="Test Product", price=10.0, stock=100)
        self.order = Order(
            order_id="123",
            owner="user123",
            product=self.product,
            quantity=2,
            subtotal=20.0
        )

    def test_order_initialization(self):
        self.assertEqual(self.order.order_id, "123")
        self.assertEqual(self.order.owner, "user123")
        self.assertEqual(self.order.product, self.product)
        self.assertEqual(self.order.quantity, 2)
        self.assertEqual(self.order.subtotal, 20.0)

    def test_get_subtotal_property(self):
        # Happy path: 2 * 10.0 = 20.0
        self.assertEqual(self.order.get_subtotal, 20.0)

    def test_get_subtotal_zero_quantity(self):
        order_zero = Order(
            order_id="124",
            owner="user124",
            product=self.product,
            quantity=0,
            subtotal=0.0
        )
        self.assertEqual(order_zero.get_subtotal, 0.0)

if __name__ == '__main__':
    unittest.main()
