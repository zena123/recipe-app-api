#  importing user model directly from models not so good
from django.test import TestCase
from django.contrib.auth import get_user_model

#  to test if elper from model can create a new user
class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """test creating new user with an email is successful"""
        email= 'test@londonappdev.com'
        password= 'Testpass123'
        user= get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))   # assert true because of password that is hashed


    def test_new_user_email_normalized(self):
        """ if the email of a new user is normalized all lowercase"""
        email = 'test@LONDONAPPDEV.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    
    # no empty or None value
    def test_new_user_invalid_email(self):
        """ test creates email with no email raises errors """
        with self.assertRaises(ValueError):     # must raise valueError to pass test
            user= get_user_model().objects.create_user(None, 'test123')
    

    def test_create_new_superuser(self):
        """
        to check that we created superuser and assigned is staff and is-supperuser
        is_superuser is included as part of PermissionsMixin
        """
        user= get_user_model().object.create_superuser(
            'test@londonappdev.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)