from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from api.users.models import UserModel

class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserModel.objects.create_user(
            email='user@example.com',
            password='password',
            first_name='User',
            last_name='Test'
        )

    def test_login_valid_credentials(self):
        data = {
            'email': 'user@example.com',
            'password': 'password'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_login_invalid_email(self):
        data = {
            'email': 'wrong@example.com',
            'password': 'password'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 401)

    def test_login_invalid_password(self):
        data = {
            'email': 'user@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 401)
