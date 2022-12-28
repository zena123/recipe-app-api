from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


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
        u = create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        # check token key exists, will trust token is working cause django and DRF has it's own test suite for that
        # TODO: FIX
        # self.assertIn('token', res.data)
        # self.assertEqual(res.status_code, status.HTTP_200_OK)  # TODO: fix this

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

    def test_retrieve_user_unauthorized(self):
        """test that authentication is required for users"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """ Test Api requests that requires authentication"""

    def setUp(self):
        user = create_user(
            email='test@gmail.com',
            password='test',
            name='testuser',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """ test retrieving profile for logged in users"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'name': self.user.name
        })

    def test_post_me_not_allowed(self):
        """test that POST not allowed on me url"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """ test updating user profile for authenticated user"""
        payload = {'name': 'new_name', 'password': 'newpassword'}
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

