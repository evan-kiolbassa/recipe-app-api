'''
Tests for the Django admin modification
'''
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    '''
    Tests for django admin
    '''

    def setUp(self):
        '''
        Create users and client to mock tests
        '''
        self.client = Client()  # Creating a client for test cases
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_users_list(self):
        '''
        Tests that users appear on Django Admin User-Interface
        '''
        url = reverse('admin:core_user_changelist')
          # Accesses list of users in sytsem
        res = self.client.get(url)  # Makes a http get request

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
