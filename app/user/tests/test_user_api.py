'''
Tests for the User API
'''
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    '''
    Create and return a new user.
    '''
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    '''
    Test the public features of the user API
    '''
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        '''
        Test for successful user creation
        '''
        # Parameter Hash Table for HTTP request
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        # Returned response object
        res = self.client.post(CREATE_USER_URL, payload)
        # Assertion that HTTP 201 code is returned
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        # Validation of successful authentication via password
        self.assertTrue(user.check_password(payload['password']))
        # Validation that there is no password key in the response object
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        '''
        Test the functionality that an error occurs when
        an account is created with an existing email
        '''
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        '''
        Tests that an error is returned when user defines
        a password that is too short (less than 5 chars)
        '''
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()  # Returns a boolean if email exists
        self.assertFalse(user_exists)
