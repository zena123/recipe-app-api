from django.test import TestCase
from django.contrib.auth import get_user_model


class TestUser(TestCase):
    def test_create_user_with_email_password(self):
        email = "zz@gmail.com"
        password = "Z12345678."
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user)

    def test_new_user_email_normalized(self):
        """ test email of new user created is normalized """
        email = "test@GMAIL.COM"
        user = get_user_model().objects.create_user(email=email)
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ test invalid user email"""
        with self.assertRaises(ValueError):
            """anything we run here should raise value error , else test will fail"""
            get_user_model().objects.create_user(None, password="test123")

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser("test@gmail.com", "test123")
        self.assertTrue(user.is_superuser)  # this comes with permissionsMixin
        self.assertTrue(user.is_staff)
