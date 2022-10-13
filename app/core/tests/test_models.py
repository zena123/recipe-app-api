from django.test import TestCase
from django.contrib.auth import get_user_model


class TestUser(TestCase):
    def test_create_user_with_email_password(self):
        email = "zz@gmail.com"
        password = "Z12345678."
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user)
