
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        url = reverse('user-register')  # Make sure this matches your URL configuration
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        
        # Print response content if the test fails
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Response content: {response.content}")