from django.test import TestCase

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class UserRegistrationTestCase(APITestCase):
    def test_user_registration(self):
        data = {'name': 'Test User', 'email': 'test@example.com', 'password': 'password123'}
        response = self.client.post('/api/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class UserDetailsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', name='Test User', password='password123')

    def test_user_details(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/details/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')

class ReferralsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='referrer@example.com', name='Referrer', password='password123')
        self.referred_user = User.objects.create_user(email='referred@example.com', name='Referred', password='password123')
        self.referral = Referral.objects.create(referrer=self.user, referred_user=self.referred_user)

    def test_referrals(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/referrals/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

