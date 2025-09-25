import unittest
from unittest.mock import Mock
from core.interfeices.usecase.criar_produto_usecase import (
    CreateProductUseCase, CreateProductRequest, CreateProductResponse,
    ListProductsUseCase, ListProductsRequest, ListProductsResponse,
    GetProductByIdUseCase, GetProductByIdRequest
)
from core.domain.entities.product import Product
from core.domain.entities.user import User, PermissionError

class TestCreateProductUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        self.use_case = CreateProductUseCase(self.mock_repo)
        self.admin_user = User(email="admin@example.com", first_name="Admin", last_name="User", is_staff=True, is_superuser=True)
        self.regular_user = User(email="user@example.com", first_name="User", last_name="Test")

    def test_execute_admin_success(self):
        request = CreateProductRequest(name="New Product", price=25.0, stock=50, is_active=True)
        created_product = Product(id="prod123", name="New Product", price=25.0, stock=50, is_active=True)
        self.mock_repo.create.return_value = created_product

        response = self.use_case.execute(request, self.admin_user)

        self.assertIsInstance(response, CreateProductResponse)
        self.assertEqual(response.id, "prod123")
        self.assertEqual(response.name, "New Product")
        self.assertEqual(response.price, 25.0)
        self.assertEqual(response.stock, 50)
        self.assertTrue(response.is_active)
        self.mock_repo.create.assert_called_once()

    def test_execute_non_admin_raises_permission_error(self):
        request = CreateProductRequest(name="New Product", price=25.0, stock=50, is_active=True)

        with self.assertRaises(PermissionError) as context:
            self.use_case.execute(request, self.regular_user)
        self.assertIn("Apenas administradores podem gerenciar produtos", str(context.exception))
        self.mock_repo.create.assert_not_called()

class TestListProductsUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        self.use_case = ListProductsUseCase(self.mock_repo)

    def test_execute_success(self):
        request = ListProductsRequest(offset=0, limit=10, search_query="test")
        products = [
            Product(id="1", name="Prod1", price=10.0, stock=10, is_active=True),
            Product(id="2", name="Prod2", price=20.0, stock=20, is_active=True)
        ]
        self.mock_repo.get_all_paginated_filtered.return_value = (products, 2)

        response = self.use_case.execute(request)

        self.assertIsInstance(response, ListProductsResponse)
        self.assertEqual(len(response.products), 2)
        self.assertEqual(response.total_items, 2)
        self.assertEqual(response.products[0].id, "1")
        self.mock_repo.get_all_paginated_filtered.assert_called_once_with(offset=0, limit=10, search_query="test")

class TestGetProductByIdUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        self.use_case = GetProductByIdUseCase(self.mock_repo)

    def test_execute_found(self):
        request = GetProductByIdRequest(product_id="prod123")
        product = Product(id="prod123", name="Found Product", price=15.0, stock=30, is_active=True)
        self.mock_repo.get_by_id.return_value = product

        response = self.use_case.execute(request)

        self.assertIsInstance(response, CreateProductResponse)
        self.assertEqual(response.id, "prod123")
        self.assertEqual(response.name, "Found Product")
        self.mock_repo.get_by_id.assert_called_once_with("prod123")

    def test_execute_not_found(self):
        request = GetProductByIdRequest(product_id="nonexistent")
        self.mock_repo.get_by_id.return_value = None

        with self.assertRaises(ValueError) as context:
            self.use_case.execute(request)
        self.assertIn("Produto não encontrado", str(context.exception))
        self.mock_repo.get_by_id.assert_called_once_with("nonexistent")

if __name__ == '__main__':
    unittest.main()
