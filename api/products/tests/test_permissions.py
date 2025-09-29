from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from api.users.models import UserModel
from api.products.models import ProductModel

class ProductPermissionsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.regular_user = UserModel.objects.create_user(
            email='user@example.com',
            password='password',
            first_name='User',
            last_name='Test'
        )
        self.admin_user = UserModel.objects.create_superuser(
            email='admin@example.com',
            password='password',
            first_name='Admin',
            last_name='Test'
        )
        self.product = ProductModel.objects.create(
            name='Test Product',
            price=10.00,
            stock=5,
            is_active=True
        )

    def test_product_list_unauthenticated(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, 401)

    def test_product_list_authenticated(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, 200)

    def test_product_create_unauthenticated(self):
        data = {
            'name': 'New Product',
            'price': 20.00,
            'stock': 10
        }
        response = self.client.post(reverse('product-list-create'), data)
        self.assertEqual(response.status_code, 401)

    def test_product_create_authenticated_non_admin(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {
            'name': 'New Product',
            'price': 20.00,
            'stock': 10
        }
        response = self.client.post(reverse('product-list-create'), data)
        self.assertEqual(response.status_code, 403)

    def test_product_create_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'name': 'New Product',
            'price': 20.00,
            'stock': 10
        }
        response = self.client.post(reverse('product-list-create'), data)
        self.assertEqual(response.status_code, 201)

    def test_product_retrieve_unauthenticated(self):
        response = self.client.get(reverse('product-retrieve', kwargs={'pk': self.product.id}))
        self.assertEqual(response.status_code, 401)

    def test_product_retrieve_authenticated_non_admin(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(reverse('product-retrieve', kwargs={'pk': self.product.id}))
        self.assertEqual(response.status_code, 403)

    def test_product_retrieve_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('product-retrieve', kwargs={'pk': self.product.id}))
        self.assertEqual(response.status_code, 200)
