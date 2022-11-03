from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse('user:token')


def create_user(**params):  # list of params
    return get_user_model().objects.create(**params)


class PublicUserApiTests(TestCase):
    """tests the user api (to public )"""

    def SetUp(self):
        self.client = APIClient

    def test_create_valid_user_success(self):
        """ test creating user with payload is successfull"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'password',
            'name': 'testName',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)  # res will have the user returned in a dict
        self.assertTrue(user.check_password('password'))
        self.assertNotIn('password', res.data)  # security check

    def test_user_exists(self):
        """ test creating user that exists  fail"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
            'name': 'test',
        }
        user = create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """test that password not less than 5 characters"""
        payload = {'email': 'test@gmail.com', 'password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # also we will make sure user not already exist
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_valid_credentials(self):
        """test token is created for a user"""
        payload = {'email': 'test@gmail.com', 'password': 'password'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        # check token key exists, will trust token is working cause django and DRF has it's own test suite for that
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ test token not created with invalid credentials"""
        create_user(email="test@gmail.com", password="testpass")
        payload = {'email': 'test@gmail.com', 'password': 'testpass1'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """test creating a token with no user invalid"""
        payload = {'email': 'test@gmail.com', 'password': 'testpass1'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ test creating token with missing data fails"""
        res = self.client.post(TOKEN_URL, {'email': 'one@gmail.com', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
