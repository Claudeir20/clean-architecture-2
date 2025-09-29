from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from api.users.models import UserModel

class UserPermissionsTestCase(TestCase):
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

    def test_user_list_unauthenticated(self):
        response = self.client.get(reverse('user-list-create'))
        self.assertEqual(response.status_code, 401)

    def test_user_list_authenticated_non_admin(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(reverse('user-list-create'))
        self.assertEqual(response.status_code, 403)

    def test_user_list_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('user-list-create'))
        self.assertEqual(response.status_code, 200)

    def test_user_create_unauthenticated(self):
        data = {
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'password123'
        }
        response = self.client.post(reverse('user-list-create'), data)
        self.assertEqual(response.status_code, 401)

    def test_user_create_authenticated_non_admin(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'password123'
        }
        response = self.client.post(reverse('user-list-create'), data)
        self.assertEqual(response.status_code, 403)

    def test_user_create_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'password123'
        }
        response = self.client.post(reverse('user-list-create'), data)
        self.assertEqual(response.status_code, 201)

    def test_user_retrieve_unauthenticated(self):
        response = self.client.get(reverse('user-retrieve', kwargs={'pk': self.regular_user.id}))
        self.assertEqual(response.status_code, 401)

    def test_user_retrieve_authenticated_non_admin(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(reverse('user-retrieve', kwargs={'pk': self.regular_user.id}))
        self.assertEqual(response.status_code, 403)

    def test_user_retrieve_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('user-retrieve', kwargs={'pk': self.regular_user.id}))
        self.assertEqual(response.status_code, 200)
