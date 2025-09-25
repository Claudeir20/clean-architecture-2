import unittest
from unittest.mock import Mock, MagicMock
from core.interfeices.usecase.criar_pedido_usecase import (
    CreateOrderUseCase, CreateOrderRequest, CreateOrderResponse,
    ListOrderUseCase, ListOrdersRequest, ListOrdersResponse
)
from core.domain.entities.order import Order
from core.domain.entities.product import Product
from core.domain.entities.user import User

class TestCreateOrderUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        self.use_case = CreateOrderUseCase(self.mock_repo)

    def test_execute_success(self):
        request = CreateOrderRequest(
            owner="user123",
            product=Product(name="Test Product", price=10.0, stock=100),
            quantity=2,
            subtotal=20.0
        )
        created_order = Order(
            order_id="order123",
            owner="user123",
            product=request.product,
            quantity=2,
            subtotal=20.0
        )
        self.mock_repo.create.return_value = created_order

        response = self.use_case.execute(request)

        self.assertIsInstance(response, CreateOrderResponse)
        self.assertEqual(response.order_id, "order123")
        self.assertEqual(response.owner, "user123")
        self.assertEqual(response.product, request.product)  # Assuming type hint is wrong
        self.assertEqual(response.quantity, 2)
        self.assertEqual(response.subtotal, 20.0)
        self.mock_repo.create.assert_called_once()

class TestListOrderUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        self.use_case = ListOrderUseCase(self.mock_repo)
        self.admin_user = User(email="admin@example.com", first_name="Admin", last_name="User", is_staff=True, is_superuser=True)
        self.regular_user = User(email="user@example.com", first_name="User", last_name="Test")

    def test_execute_with_admin_user(self):
        request = ListOrdersRequest(offset=0, limit=10, search_query=None)
        orders = [
            Order(order_id="1", owner="user1", product=Product(name="Prod1", price=10.0, stock=10), quantity=1, subtotal=10.0),
            Order(order_id="2", owner="user2", product=Product(name="Prod2", price=20.0, stock=10), quantity=2, subtotal=40.0)
        ]
        self.mock_repo.get_all_paginated_filtered.return_value = (orders, 2)

        response = self.use_case.execute(request, self.admin_user)

        self.assertIsInstance(response, ListOrdersResponse)
        self.assertEqual(len(response.orders), 2)
        self.assertEqual(response.total_items, 2)
        self.assertEqual(response.orders[0].order_id, "1")
        self.assertEqual(response.orders[0].product, "Prod1")  # name
        self.assertEqual(response.orders[0].subtotal, 10.0)  # get_subtotal
        self.mock_repo.get_all_paginated_filtered.assert_called_once_with(offset=0, limit=10, search_query=None)

    def test_execute_with_regular_user_filters_orders(self):
        request = ListOrdersRequest(offset=0, limit=10, search_query=None)
        orders = [
            Order(order_id="1", owner=self.regular_user.id, product=Product(name="Prod1", price=10.0, stock=10), quantity=1, subtotal=10.0),
            Order(order_id="2", owner="other_user", product=Product(name="Prod2", price=20.0, stock=10), quantity=2, subtotal=40.0)
        ]
        self.mock_repo.get_all_paginated_filtered.return_value = (orders, 2)

        response = self.use_case.execute(request, self.regular_user)

        self.assertEqual(len(response.orders), 1)  # Only own order
        self.assertEqual(response.orders[0].order_id, "1")
        self.assertEqual(response.total_items, 1)  # Filtered count

if __name__ == '__main__':
    unittest.main()
